# cs6170-final

## Installation
To install, make sure that `ffmpeg` and `hdf5` is installed. Since neither of these were installed for me, I used 
``` bash
sudo apt update
sudo apt install ffmpeg
sudo apt-get install libhdf5-serial-dev
```` 
Additionally, for the python portion, I used `pip install h5py` for evenutal reading from file since I did not have that python module. After installing all the above software, `cd` to the directory `simulate` and type `make`. This creates the executable `simulate`. `simulate` takes two arguments. The first is the number of timesteps to use when generating, the second is the time between timesteps until data is written to file in the `./fields` directory. For example, I used `./simulate 1000 10` to generate 100 stages of the simulation. After this, run `python3 plot.py` and this will generate a video simulation. 

This code is borrowed from https://github.com/ctjacobs/compressible-rayleigh-taylor-instability. I modified it to not require CUDA and to take command line arguments since that seemed more of a headache than we needed. 
