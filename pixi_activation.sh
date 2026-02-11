#!/bin/bash
# Pixi activation script for PyELEGANT
# Prepend ~/.local/lib to LD_LIBRARY_PATH so mpi4py 4.x can find the libmpi.so.12
# symlink created by "pixi run fix-mpi4py-soname". This also propagates to SLURM
# compute nodes when jobs are submitted from within this pixi shell.
export LD_LIBRARY_PATH="${HOME}/.local/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
