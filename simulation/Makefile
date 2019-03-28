# HDF5
HDF5_INCLUDE=/usr/include/hdf5/serial
HDF5_LIB=/usr/lib/x86_64-linux-gnu/hdf5/serial/

# C compiler
CC=gcc -std=c99
CCFLAGS=-I. -I$(HDF5_INCLUDE) -L$(HDF5_LIB)

rt: rt.c grid.c
	$(CC) -o simulate rt.c grid.c $(CCFLAGS) -lm -lhdf5
