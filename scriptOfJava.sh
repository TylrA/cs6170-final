#!/bin/bash

# Check the SRCPATH and DESTPATH to make sure they are pointing to the correct directories, then run script and watch for stalls. Every time it stalls for more than a few seconds, you will probably have to kill it with the kill command. Use ps a to find the right java program pid. These unfinished boundaries will have to be computed later using repair.sh and repair2.sh

# SRCPATH should be set to the mother directory of the raw images from palabos. This directory should contain directories {gifs$idx | idx = 0, 1, 2, 3}, each of which should contain directories {sim$idx | idx = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.
SRCPATH=sim_data

# DESTPATH should be set to the mother destination directory.
DESTPATH=point_clouds/new

SETIDX=0

while [ $SETIDX -le 3 ]
do
    echo $SETIDX

    SIMIDX=0
    while [ $SIMIDX -lt 10 ]
    do
	TIMEIDX=1000
	
	UPPERTIMEBOUND=6000
	if [ $SETIDX -eq 2 ]
	then
	    UPPERTIMEBOUND=8000
	elif [ $SETIDX -eq 3 ]
	then
	    UPPERTIMEBOUND=7600
	fi
	
	mkdir -p $DESTPATH/gifs$SETIDX/sim$SIMIDX
	
	while [ $TIMEIDX -le $UPPERTIMEBOUND ]
	do
	    echo Starting gifs$SETIDX sim$SIMIDX timestamp$TIMEIDX
	    java -jar java_tool.jar -unig 6 $SRCPATH/gifs$SETIDX/sim$SIMIDX/rho_light_00$TIMEIDX.gif $DESTPATH/gifs$SETIDX/sim$SIMIDX/image_$TIMEIDX.png $DESTPATH/gifs$SETIDX/sim$SIMIDX/points_$TIMEIDX.txt
	    TIMEIDX=$((TIMEIDX+100))
	done

	((SIMIDX++))
    done
	
    ((SETIDX++))
done

