# Code Directory
Please see our report for an explanation of these strategies.
## /gametheory/
Contains code for the weighted running average strategy. See gametheory.py for strategy classes.
## /linear_optimization/

## /oneshot/
Relevant Files:
* `oneshot.py` contains the oneshot algorithm 
* `multishot.py` contains the multishot algorithm
## /randomForest/

## /vwprediction/
Contains code for the Vowpal Wabbit strategy.  

Relevant Files:
* `formatting_script.py` formats our raw data into files with trainable examples for VW. 
* `plot.ipynb` contains graphs of data used in finding the best multipliers and models.
* `simulate.py` contains the `VWSimulator` class, which simulates revenue gained by using a VW model.
* `testing.py` is used to tune for the optimal multiplier values and models.
* `tuning.py` was used to train VW models on bids between two times.
* The `models` folder contains the final models we used, with 1-5 passes through data.
## /simulator/
This is where the simulator engine is located. The methods are detailed by the docstrings in simulator.py.
## /results/
This directory contains output from experiments, in addition to the generating code.
