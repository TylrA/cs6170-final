#!/usr/bin/env bash
if python3 Main.py
then
    cd ../
    exit 0
else
    printf "An error occurred somewhere in the program\n"
    cd ../
    exit 1
fi
