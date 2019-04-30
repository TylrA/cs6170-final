#!/bin/bash

# SRCPATH should be set to the mother directory of the raw images from palabos. This directory should contain directories {gifs$idx | idx = 0, 1, 2, 3}, each of which should contain directories {sim$idx | idx = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9}.
SRCPATH=../../final_data/original/gifs2

# DESTPATH should be set to the mother destination directory.
DESTPATH=point_clouds

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
	
	mkdir -p $DESTPATH/gif$SETIDX/sim$SIMIDX
	
	while [ $TIMEIDX -le $UPPERTIMEBOUND ]
	do
	    echo Starting gifs$SETIDX sim$SIMIDX timestamp$TIMEIDX
	    java -jar java_tool.jar -unig 6 $SRCPATH/gifs$SETIDX/sim$SIMIDX/rho_light_00$TIMEIDX.gif $DESTPATH/gif$SETIDX/sim$SIMIDX/image_$TIMEIDX.png $DESTPATH/gif$SETIDX/sim$SIMIDX/points_$TIMEIDX.txt
	    TIMEIDX=$((TIMEIDX+100))
	done

	((SIMIDX++))
    done
	
    ((SETIDX++))
done

