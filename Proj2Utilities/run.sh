#!/usr/bin/env bash
printf "Attempting to build local Ripser\n"
cd ./ripser
if make
then
    printf "Ripser successfully installed\n"
    cd ../
else
    printf "Error installing Ripser\n"
    cd ../
    exit 1
fi

printf "Attempting to interface with Hera\n"
cd ./hera/geom_bottleneck
if  c++ -std=c++11 hera_bottleneck_interface.cpp -o hera_bottleneck_interface
then
    printf "Successfully built Hera bottleneck interface\n"
    cd ../geom_matching
    if c++ -std=c++1y hera_wasserstein_interface.cpp -o hera_wasserstein_interface -lpthread
    then
        printf "Successfully build Hera Wasserstein interface\n"
        cd ../../
    else
        printf "Error building Wasserstein interface\n"
        cd ../../
        exit 1
    fi
else
    printf "Error building Hera bottleneck interface. Is boost installed? Is the c++11 compiler installed?\n"
    cd ../../
    exit 1
fi

#printf "\nWould you like to use existing datasets? y/n\n"
#read choice
#if [[ "$choice" == "n" ]];
#then
#    printf "Are you sure? This may take around 10-15 minutes dependent on your machine. y/n\n"
#    read choice
#    if [[ "$choice" == "y" ]];
#    then
#        choice="n"
#    fi
#fi
#
#if [[ "$choice" == "n" ]];
#then
#    cd ./Data
#    rm -rf ./BottleneckDistances
#    rm -rf ./ImageBarcodes
#    rm -rf ./ImageBoundaries
#    rm -rf ./WassersteinDistances
#
#    mkdir ./BottleneckDistances
#    mkdir ./ImageBarcodes
#    mkdir ./ImageBoundaries
#    mkdir ./WassersteinDistances
#    cd ./ImageBarcodes
#    mkdir ./dim0
#    mkdir ./dim1
#    cd ../../
#fi

if python3 Main.py
then
    cd ../
    exit 0
else
    printf "An error occurred somewhere in the program\n"
    cd ../
    exit 1
fi
