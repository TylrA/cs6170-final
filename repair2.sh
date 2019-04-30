#!/bin/bash

SRCPATH=../../final_data/original/gifs2
DESTPATH=point_clouds

SETIDX=$1
SIMIDX=$2
TIMEIDX=$3
RADIUS=$4
BLUR=$5
STARTPOS=$6

java -jar java_tool2.jar -unirichcustom $RADIUS $BLUR $STARTPOS $SRCPATH/gifs$SETIDX/sim$SIMIDX/rho_light_00${TIMEIDX}00.gif $DESTPATH/gifs$SETIDX/sim$SIMIDX/image_${TIMEIDX}00.png $DESTPATH/gifs$SETIDX/sim$SIMIDX/points_${TIMEIDX}00.txt

gwenview $DESTPATH/gifs$SETIDX/sim$SIMIDX/image_${TIMEIDX}00.png
