#!/usr/bin/env bash

rm -rf ./gifs
mkdir ./gifs

cd ./palabos-v2.0r0/examples/showCases/multiComponent2d
if ! make
then 
    print "An error occured during compilation.\n"
    cd ../../../../
    exit 1
else
    cd ../../../../
fi
cd ./gifs

for i in 0 1 2 3 4 5 6 7 8 9
do
    rm -rf "./gifs$i"
    mkdir "./gifs$i"
    cd "./gifs$i"
    for j in 0 1 2 3 4 5 6 7 8 9
    do
	mkdir "./sim$j"
    done
    cd ../
done

rho1s=(1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9)
rho0s=(1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1)

cd ../palabos-v2.0r0/examples/showCases/multiComponent2d
for i in 0 1 2 3 4 5 6 7 8 9
do
    for j in 0 1 2 3 4 5 6 7 8 9
    do
        if ! ./rayleighTaylor2D 16000 ${rho1s[j]} ${rho0s[j]} "./gifs$i/sim$j"
        then
            printf "An error occured generating simulation\n"
            cd ../../../../
            exit 1
        fi
    done
done
cd ../../../../
