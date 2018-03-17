module DecisionTrees.RandomForest where

import Control.Monad
import Control.Monad.Random

import DecisionTrees.DecisionTree as D
import Util.Util

newtype Forest a b = Forest [D.DTree a () b] deriving (Show)

randomForest :: (Ord a, Ord b, RandomGen g) =>
                 Int -- N trees
              -> Int -- N attributes per tree
              -> (a -> b) -- target attribute
              -> [Att a] -- Attributes to classify on
              -> [a] -- observations
              -> Rand g (Forest a b)
randomForest nTree nAtt target atts as = fmap Forest (replicateM nTree go) where
    go = do atts' <- sampleMany nAtt atts
            as' <- sampleWithReplacement (length as) as
            return $ D.fitTree target atts' as'

decide :: Ord b => Forest a b -> a -> b
decide (Forest trees) a = mode $ map (`D.decide` a) trees
