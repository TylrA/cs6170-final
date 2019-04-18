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

#rho1s=(1.0 1.2 1.4 1.6 1.8)
#rho0s=(1.0 0.8 0.6 0.4 0.2)
rho1s=(1.0 0.8 1.0 0.8 1.0 0.8)
rho0s=(0.0 0.0 0.2 0.2 0.4 0.4)

for i in 0 1 2 3 4 5
do
    rm -rf "./gifs$i-${rho1s[i]}-${rho0s[i]}"
    mkdir "./gifs$i-${rho1s[i]}-${rho0s[i]}"
    cd "./gifs$i-${rho1s[i]}-${rho0s[i]}"
    for j in 0 1 2 3 4 5 6 7 8 9
    do
	mkdir "./sim$j"
    done
    cd ../
done

cd ../palabos-v2.0r0/examples/showCases/multiComponent2d
for i in 0 1 2 3 4 5
do
    for j in 0 1 2 3 4 5 6 7 8 9
    do
        if ! ./rayleighTaylor2D 10000 ${rho1s[i]} ${rho0s[i]} "./gifs$i-${rho1s[i]}-${rho0s[i]}/sim$j"
        then
            printf "An error occured generating simulation\n"
            cd ../../../../
            exit 1
        fi
    done
done
cd ../../../../
