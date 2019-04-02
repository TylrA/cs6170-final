#!/usr/bin/env bash

rm -rf ./vtis
mkdir ./vtis

cd ./palabos-v2.0r0/examples/showCases/multiComponent3d
if ! make
then 
    print "An error occured during compilation.\n"
    cd ../../../../
    exit 1
fi

if ! ./rayleighTaylor3D
then
    printf "An error occured generating simulation\n"
    cd ../../../../
    exit 1
else
    cd ../../../../
fi 

