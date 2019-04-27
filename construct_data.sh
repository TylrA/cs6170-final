#!/usr/bin/env bash
cd ./simulation/
bash ./run.sh     # Create simulation. This takes a VERY LONG time. Approx 12 hours.
cd ../

###################################
#    CONSTRUCT BOUNDARIES HERE    #
###################################

# Generate critical diagrams
cd ./final/
python3 GenerateCriticalDiagrams.py
cd ../

# Install local ripser and hera interfaces
cd ./Proj2Utilities/
bash ./install.sh
cd ../

# Run ripser on image boundaries
cd ./Proj2Utilities/Part1/
python3 RunRipser
cd ../

# Compute bottleneck and wasserstein distances for critical diagrams and store
cd ./Proj2Utilities/Part1/
python3 ComputeBottWass.py bubble_backup
python3 ComputeBottWass.py ripser_backup
cd ../../



