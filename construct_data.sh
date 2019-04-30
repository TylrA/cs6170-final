#!/usr/bin/env bash
#cd ./simulation/
#bash ./simulate.sh     # Create simulation. This takes a VERY LONG time. Approx 12 hours.
#cd ../

#bash ./scriptOfJava.sh # Extracts the boundary surface. Please note that this often stalls. If you want to compute the boundaries yourself, you will often have to kill running java programs, and compute them individually with ./repair.sh and ./repair2.sh. See all three scripts for more details.

# Generate critical diagrams
cd ./final/
python3 GenerateCriticalDiagrams.py
cd ../

# Install local ripser and hera interfaces
cd ./Proj2Utilities/
bash ./install.sh
cd ../

# Move last-stage simulation image to correct folder for ripser
cd ./final/smoothed_boundary_points/
python3 MoveFiles.py
cd ../../

# Run ripser on image boundaries
cd ./Proj2Utilities/Part1/
python3 RunRipser.py
cd ../../

# Compute bottleneck and wasserstein distances for critical diagrams and store
cd ./Proj2Utilities/Part1/
python3 ComputeBottWass.py bubble_backup
python3 ComputeBottWass.py ripser_backup
cd ../../



