#!/bin/bash

# This script takes 6 parameters:
# The first parameter is the index of the densities (0, 1, 2, or 3), which corresponds to the gifs0, gifs1, gifs2, and gifs3 directories.
# The second parameter is the index of the simulation within one gifs index.
# The third parameter is the time interval index divided by 1000.
# The fourth parameter is the radius between points of the boundary extraction algorithm.
# The fifth parameter is the blur factor for the image to produce the difference image.
# The sixth parameter is the x offset of the first point. It will try to find the isosurface by taking the maximum value pixel in the column with this offset.

# NOTE: the blur factor should be an odd number, and it specifies the side length of the squares around pixels in the image that should be blurred together. For instance, if the blur factor was 5, then each pixel would be blurred with its 24 neighbors in the 5 x 5 square centered on the given pixel.

# EXAMPLE
# ./repair.sh 1 4 43 6 7 150
# This would attempt to run the java boundary extraction tool on gifs1/sim4/rho_light_004300.gif with a radius of 6 between points, and a blur factor of 7. It will start at x = 150, and choose the maximum value pixel in that column as the first point of the isosurface.

# NOTE: expect to try several configurations before one accurately tracks the isosurface.

# SRCPATH should point to the mother directory of the raw images produced by palabos. It should contain directories {gifs$idx | idx = 0, 1, 2, 3}, each of which should contain directories {sim$idx | idx = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
SRCPATH=sim_data

# DESTPATH should point to the destination directory.
DESTPATH=point_clouds/new

SETIDX=$1
SIMIDX=$2
TIMEIDX=$3
RADIUS=$4
BLUR=$5
STARTPOS=$6

java -jar java_tool2.jar -unirichcustom $RADIUS $BLUR $STARTPOS $SRCPATH/gifs$SETIDX/sim$SIMIDX/rho_light_00${TIMEIDX}00.gif $DESTPATH/gifs$SETIDX/sim$SIMIDX/image_${TIMEIDX}00.png $DESTPATH/gifs$SETIDX/sim$SIMIDX/points_${TIMEIDX}00.txt

gwenview $DESTPATH/gifs$SETIDX/sim$SIMIDX/image_${TIMEIDX}00.png
