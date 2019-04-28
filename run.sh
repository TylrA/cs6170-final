#!/usr/bin/env bash
printf "\nChoose an option to run\n"
printf "1. Mixing Specie Classification With Critical Diagrams\n"
printf "2. Mixing Specie Classification With Persistence Diagrams\n"

rm -rf ./Proj2Utilities/Data/BottleneckDistances
rm -rf ./Proj2Utilities/Data/ImageBarcodes
rm -rf ./Proj2Utilities/Data/WassersteinDistances
rm -rf ./Proj2Utilities/Data/ImageBoundaries

read choice
if [[ "$choice" == "1" ]];
then
    cp -r ./DataBackup/bubble_backup/BottleneckDistances/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/bubble_backup/ImageBarcodes/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/bubble_backup/ImageBoundaries/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/bubble_backup/WassersteinDistances/ ./Proj2Utilities/Data/
else
    cp -r ./DataBackup/ripser_backup/BottleneckDistances/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/ripser_backup/ImageBarcodes/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/ripser_backup/ImageBoundaries/ ./Proj2Utilities/Data/
    cp -r ./DataBackup/ripser_backup/WassersteinDistances/ ./Proj2Utilities/Data/
fi

cd ./Proj2Utilities/
if python3 Main.py "$choice"
then
    cd ../
    exit 0
else
    printf "An error occurred somewhere in the program\n"
    cd ../
    exit 1
fi
cd ../
