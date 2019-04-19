#!/usr/bin/env bash

rm -rf ./gifs3
mkdir ./gifs3

cd ./palabos-v2.0r0/examples/showCases/multiComponent2d
if ! make
then 
    print "An error occured during compilation.\n"
    cd ../../../../
    exit 1
else
    cd ../../../../
fi
cd ./gifs3

for i in 1 2 3 4 5 6 6 8 9 10
do
    rm -rf "./gifs3$i"
    mkdir "./gifs3$i"
done

rho1s=(1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9)
rho0s=(1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1)

cd ../palabos-v2.0r0/examples/showCases/multiComponent2d
for i in 1 2 3 4 5 6 7 8 9 10
do
    for j in 0 1 2 3 4 5 6 7 8 9
    do
        if ! ./rayleighTaylor2D 160000 ${rho1s[j]} ${rho0s[j]} "/gifs3$i"
        then
            printf "An error occured generating simulation\n"
            cd ../../../../
            exit 1
        else
            cd ../../../../
        fi
    done
done
