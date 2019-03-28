#!/usr/bin/env bash

if ! make
then
    printf "An error occured during compilation\n"
    exit 1
fi

rm -rf ./fields
mkdir ./fields

printf "\nPlease enter number of desired timesteps\n"
read numTimeSteps
printf "\nPlease enter interval of timesteps before writing to file\n"
read intervalSize

if ! ./simulate "$numTimeSteps" "$intervalSize"
then
    printf "An error occured generating simulation\n"
    exit 1
fi 

if ! python3 plot.py
then
    printf "An error occurred somewhere in the program\n"
    exit 1
fi
