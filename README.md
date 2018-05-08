# Repository Contents
## `Dynamic Price Floors - Report.pdf`
A 16-page report containing explanations of our most promising strategies, and results.
## `DPF Final Deliverable Presentation.pdf`
Our final deliverable presentation, outlining the content of the report.
## `simulator_comparator.py`
See this file for an example of how to use our simulator to reproduce results.
## `/simulator/`
This is where the simulator engine is located. The methods are detailed by the docstrings in simulator.py.
## `/results/`
This directory contains output from experiments, in addition to the associated test code.
## `/gametheory/`
Contains code for the weighted running average strategy. See `gametheory.py` for strategy classes.
## `/linear_optimization/`
Relevant Files:
* `clever_brute_force.py` brute force solver
* `linear_heuristic.py` linear heuristic approximation method
* `linear_programming.py` old linear programming approach (does not work)
## `/oneshot/`
Relevant Files:
* `oneshot.py` contains the oneshot algorithm 
* `multishot.py` contains the multishot algorithm
## `/randomForest/`
Relevant Files:
* `randomForestSimulator.py` Simulator file
* `tensorflowVersion/Random Forest Tensorflow.ipynb` Research notebook
* `randomForest/` Scrapped haskell version, never tested
## `/vwprediction/`
Contains code for the Vowpal Wabbit strategy.  

Relevant Files:
* `formatting_script.py` formats our raw data into files with trainable examples for VW. 
* `plot.ipynb` contains graphs of data used in finding the best multipliers and models.
* `simulate.py` contains the `VWSimulator` class, which simulates revenue gained by using a VW model.
* `testing.py` is used to tune for the optimal multiplier values and models.
* `tuning.py` was used to train VW models on bids between two times.
* The `models` folder contains the final models we used, with 1-5 passes through data.
## `/running_average/`
Includes optimized classes in `runnning_average.py` for experimenting with global and separated running averages.
## `/scripts/`
Contains code that formats the data from `s3://adsnative-sigmoid`

Relevant Files:
* `filterer.py` filters out direct auctions and redundant bid lines
* `combiner.py` reduces the number of files so as to reduce GET requests to S3
