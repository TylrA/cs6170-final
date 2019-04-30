# cs6170-final

The final project has many steps of pre-processing. This readme explains how
to construct the data and then how to run the tests. If you do not wish to 
construct the data, pre-processed data is included so you may skip to
the Testing section below.

## Data Construction

To generate data for the Testing section below, first, `cd` to the 
directory `/cs6170-final`. Then run
```bash
bash ./construct_data.sh
```
Keep in mind that this will take a long time, perhaps an entire day. If you 
wish to test portions of this construction, the bash script is simple
enough that you will know which portion to comment out. Simulation and 
boundary extraction take the longest and they are the first two portions
in the bash script. The rest may take about two hours.

## Testing
To reproduce the results of the test, make sure you are in the `/cs6170-final`
directory and run
```bash
bash ./run.sh
```
This will start a script to reproduce the results of the report. Simply follow
the prompts. This script essentially runs project 2 for the class which serves
as a useful comparison between persistent homology of the boundary images and
critical diagrams. All the parts and subparts referenced in the program exactly
correspond to the parts and subparts of Project 2.

## Source Code

The java source code for the boundary extraction is found in `simulation/point_extraction/f`.