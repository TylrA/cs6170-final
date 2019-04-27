# cs6170-final

The final project has many steps of pre-processing. This readme explains how
to construct the data and then how to run the tests. If you do not wish to 
construct the data, pre-processed data is included so you may skip to
the Testing section below.

## Data Construction

First, `cd` to the directory `/cs6170-final`. 
To run the simulation and generate the images, run
```bash
cd simulation; bash ./run.sh
```
This will take quite a while. It took us around 12 or more hours on the CADE 
machines. After this is done, `cd` again back to `/cs6170-final`. 

Next comes the boundary extraction. 

INSERT HOW TO EXTRACT BOUNDARIES HERE

After boundaries have been extracted, to generate critical diagrams, run
```python
python3 GenerateCriticalDiagrams.py
```
Status bars will show you the progress. This may take a couple hours.

Next we must install local versions of Ripser and Hera interfaces. To do so,
`cd` again back to `/cs6170-final` and then type
```bash
cd Proj2Utilities; bash ./install.sh
```

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