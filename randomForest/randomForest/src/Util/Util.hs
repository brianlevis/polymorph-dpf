{-# LANGUAGE BangPatterns #-}

module Util.Util where

import qualified Data.List as L
import qualified Data.Map as M
import qualified Data.Ord as O
import qualified System.Random as R

import Control.Concurrent.STM
import Control.DeepSeq
import Control.Monad
import Control.Monad.Error
import Control.Monad.Random
import Data.Map (Map, (!))
import System.CPUTime
import System.Random
import System.Timeout

posInf :: Fractional a => a
posInf = 1/0

negInf :: Fractional a => a
negInf = -1/0

mean :: Fractional a => [a] -> a
mean xs = total  / fromInteger len where
    (total, len) = L.foldl' k (0, 0) xs
    k (!s, !n) x = (s+x, n+1)

no :: Maybe a -> Bool
no Nothing = True
no _ = False

fst3 :: (a, b, c) -> a
fst3 (a, _, _) = a

snd3 :: (a, b, c) -> b
snd3 (_, b, _) = b

thd3 :: (a, b, c) -> c
thd3 (_, _, c) = c

enum :: (Enum a, Bounded b) => [b]
enum = [minBound .. maxBound]

notNull :: [a] -> Bool
notNull = not . null

elemsAt :: [a] -> [Int] -> [a]
elemsAt as is = map (as!!) is

insert :: Int -> a -> [a] -> [a]
insert 0 n (_:xs) = n : xs
insert i n (x:xs) = x : insert (i - 1) n xs

deleteEvery :: Eq a => a -> [a] -> [a]
deleteEvery [] = []
deleteEvery x (y:ys) = if y == x then deleteEvery x ys else y : deleteEvery x ys

deleteAll :: Eq a => [a] -> [a] -> [a]
deleteAll xs [] = []
deleteAll xs (y:ys) = if y `elem` xs then deleteAll xs ys else y:deleteAll xs ys

orderedPairs :: [a] -> [(a, a)]
orderedPairs xs = [(x, y) | x <- xs, y <- xs]

unorderedPairs :: [a] -> [(a, a)]
unorderedPairs [] = []
unorderedPairs (x:xs) = [(x, y) | y <- xs] ++ unorderedPairs xs

points :: [a] -> [(a, [a])]
points [] = []
points (a:as) = (a, as) : [(b, bs) | (b, bs) <- points as]

allEqual :: Eq a => [a] -> Bool
allEqual (a:as) = all (==a) as

mode :: Ord b => [b] -> b
mode xs = fst $ L.maximumBy (0.comparing snd) $
    map (\a -> (head a, length a)) $
    L.group $ L.sort xs

isSubset :: Eq a => [a] -> [a] -> Bool
xs `isSubset` ys = all (`elem` ys) xs

enumerate :: [a] -> [(Int, a)]
enumerate = zip [0..]

countIf :: (a -> Bool) -> [a] -> Int
countIf p xs = length (filter p xs)

argMin :: Ord b => [a] -> (a -> b) -> a
argMin xs f = L.minimumBy (0.comparing f) xs

argMinList :: Ord b => [a] -> (a -> b) -> [a]
argMinList xs f = map (xs!!) indices where
    ys = map f xs
    minVal = minimum ys
    indices = L.findIndices (==minVal) ys

argMinRandom :: (Ord b, RandomGen g) => g -> [a] -> (a -> b) -> (a, g)
argMinRandom g xs f = randomChoice g (argMinList xs f)

argMinRandomIO :: Ord b => [a] -> (a -> b) -> IO a
argMinRandomIO xs f = getStdGen >>= \g -> return $ fst $ argMinRandom g xs f

argMax :: (Ord b, Num b) => [a] -> (a -> b) -> a
argMax xs f = argMin xs (negate . f)

argMaxList :: (Ord b, Num b) -> [a] -> (a -> b) -> [a]
argMaxList xs f = argMinList xs (negate . f)

argMaxRandom :: (Ord b, Num b, RandomGen g) => g -> [a] -> (a -> b) -> (a, g)
argMaxRandom g xs f = argMinRandom g xs (negate . f)

argMaxRandomIO :: (Ord b, Num b) => [a] -> (a -> b) -> a
argMaxRandomIO xs f = argMinRandomIO xs (negate . f)

listToFunction :: (Ord a) => [(a, b)] -> a -> b
listToFunction xs = (M.fromList xs !)

transpose :: [[a]] -> [[a]]
transpose xs = if or (map null xs)
    then []
    else let heads = map head xs
             tails = map tail xs
         in heads : transpose tails

(%!) :: Eq a => [(a, b)] -> a -> b
(%!) as a = case lookup a as of
    Nothing -> error "Variable not found in list"
    Just b -> b

bools :: Int -> [[Bool]]
bools 0 = [[]]
bools n = do
    x <- [True, False]
    xs <- bools (n - 1)
    return x:xs

subsets :: [a] -> [[a]]
subsets = filterM $ const [True, False]

lstrip :: String -> String
lstrip = dropWhile (`elem` " \t")

rstrip :: String -> String
rstrip = reverse . lstrip . reverse

strip :: String -> String
strip = rstrip . lstrip

commaSep :: [String] -> String
commaSep xs = concat $ L.intersperse "," xs

mkUniversalMap :: Ord k => [k] -> a -> Map k a
mkUniversalMap ks a = M.fromList $ zip ks (repeat a)

whenM :: Monad m => m Bool -> m () -> m ()
whenM test s = test >>= \p -> when p s

ifM :: Monad m => m Bool -> m a -> m a -> m a
ifM test a b = test >>= \p -> if p then a else b

untilM :: Monad m => (t -> Bool) -> m t -> (t -> m ()) -> m ()
untilM predicate prompt action = do
    result <- prompt
    if predicate result
        then return ()
        else action result >> untilM predicate prompt action

ignoreResult :: Monad m => m a -> m ()
ignoreResult c = c >> return ()

trapError :: MonadicError e m => m () -> m ()
trapError c = c `catchError` \_ -> return ()

selectOne :: Eq a => RandomGen g => [a] -> Rand g (a, [a])
selectOne xs = do
    let n = length xs
    i <- getRandomR (0,n-1)
    let x = xs !! i
    return (x, L.delete x xs)

selectMany' :: Eq a => RandomGen g => Int -> [a] -> Rand g ([a], [a])
selectMany' 0 xs = return ([], xs)
selectMany' k xs = do
    (y,  xs')  <- selectOne xs
    (ys, xs'') <- selectMany' (k-1) xs'
    return (y:ys, xs'')

selectMany :: Eq a => RandomGen g => Int -> [a] -> Rand g [a]
selectMany k = fmap fst . selectMany' k

sampleOne :: RandomGen g => [a] -> Rand g a
sampleOne [] = error "Empty list -- SAMPLEONE"
sampleOne xs = do
    n <- getRandomR (0, length xs - 1)
    return (xs !! n)

sampleWithReplacement :: RandomGen g => Int -> [a] -> Rand g [a]
sampleWithReplacement 0 xs = return []
sampleWithReplacement n xs = do
    y  <- sampleOne xs
    ys <- sampleWithReplacement (n-1) xs
    return (y:ys)

getRandomEnum :: (RandomGen g, Enum a, Bounded a) => Int -> Rand g a
getRandomEnum i = getRandomR (0,i-1) >>= return . toEnum

randomChoice :: RandomGen g => g -> [a] -> (a, g)
randomChoice g [] = error "Empty list -- RANDOMCHOICE"
randomChoice g xs = (xs !! n, next) where
    (n, next) = randomR (0, length xs - 1) g

randomChoiceIO :: [a] -> IO a
randomChoiceIO xs = getStdGen >>= \g -> return $ fst $ randomChoice g xs

probability :: (RandomGen g, Random a, Ord a, Num a) => g -> a -> (Bool, g)
probability g p = if p' < p then (True, g') else (False, g') where
    (p', g') = R.randomR (0,1) g

probabilityIO :: (R.Random a, Ord a, Num a) => a -> IO Bool
probabilityIO p = randomIO >>= \q -> return $! if q < p then True else False

readPrompt :: IO String
readPrompt = putStr "> " >> getLine

timed :: (NFData a) => a -> IO (a, Int)
timed x = do
    t1 <- getCPUTime
    r  <- return $!! x
    t2 <- getCPUTime
    let diff = fromIntegral (t2 - t1) `div` 1000000
    return (r, diff)

timeLimited :: (NFData a) => Int -> [a] -> IO [a]
timeLimited t xs = do
    v <- newTVarIO []
    timeout t (forceIntoTVar v xs)
    readTVarIO v

forceIntoTVar :: (NFData a) => TVar [a] -> [a] -> IO ()
forceIntoTVar v xs = mapM_ (forceCons v) xs

forceCons :: (NFData a) => TVar [a] -> a -> IO ()
forceCons v x = x `deepseq` atomically $ modifyTVar2 v (x:)

modifyTVar2 :: TVar a -> (a -> a) -> STM ()
modifyTVar2 v f = readTVar v >>= writeTVar v . f
