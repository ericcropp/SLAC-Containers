#!/bin/bash
#SBATCH --image=docker:slacact/impact-bmad:nersc
#SBATCH --nodes=1
#SBATCH --qos=regular
#SBATCH --constraint=cpu

srun -n 32 shifter python3 myPythonScript.py args