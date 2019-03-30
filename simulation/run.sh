#!/usr/bin/env bash

rm -rf ./gifs
mkdir ./gifs

cd ./palabos-v2.0r0/examples/showCases/multiComponent2d
if ! make
then 
    print "An error occured during compilation.\n"
    cd ../../../../
    exit 1
fi

if ! ./rayleighTaylor2D
then
    printf "An error occured generating simulation\n"
    cd ../../../../
    exit 1
else
    cd ../../../../
fi 

