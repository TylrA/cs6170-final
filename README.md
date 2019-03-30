# cs6170-final

## Installation
There are a few libraries I had to install. Unfortunately I do not remember which ones but it was not difficult to do when you look at the compilation errors and do a little googling. I do remember the strangest library we need is eigen3 (I only had to download 3 libraries). To install eigen3, simply use  
``` 
sudo apt update
sudo apt install libeigen3-dev
```` 
The code is a modified version of the original which can be found here: http://www.palabos.org/download-ql. A direct download would not build the simulation we needed so this git version should be ok (it works for me at least). Also, after installing the necessary libraries, there is a bash script that does some additional cleanup of files between simulations and constructs the images. To use it, just run `bash ./run.sh`. If `.` is the root directory of the project, then `cd ./simulation` to get to the bash script. 

The simulation spits out a bunch of `.gifs` in the directory `./simulation/gifs` which we can use for boundary extraction and can make into a movie if we wish. Lastly, for some reason it generates two types of `.gifs` depending on light and heavy fluids. I have not tried removing one of which because I am lazy and didn't want to break anything. 

When you run the the script, after compilation you will be prompted asking how many iterations you would like to run. In order to see the simulation develop, choose around 10000. The default was 16000 but that seemed like overkill.
