function jupyter() {
    SCRATCH_PATH=$(echo $SCRATCH)
    apptainer exec --nv -B /sdf,/fs,/sdf/scratch,/lscratch --env SCRATCH=$SCRATCH_PATH ${APPTAINER_IMAGE_PATH} jupyter --no-browser --allow-root --notebook-dir=/opt/notebooks --port=5555 "$@"
}

jupyter


#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=FACET
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --pty /bin/bash

# Load necessary modules
#module load singularity

# Define the path to your Singularity image
APPTAINER_IMAGE_PATH="/sdf/scratch/users/s/sanjeev/singularity/impact-bmad_latest.sif"

function jupyter() {
    SCRATCH_PATH=$(echo $SCRATCH)
    apptainer exec --nv -B /sdf,/fs,/sdf/scratch,/lscratch --env SCRATCH=$SCRATCH_PATH ${APPTAINER_IMAGE_PATH} jupyter --no-browser --allow-root --notebook-dir=/opt/notebooks --port=5555 "$@"
}


jupyter



------------------------------------------------

singularity pull docker://slacact/impact-bmad
-------------------
export APPTAINER_CACHEDIR=${SCRATCH}/.apptainer

APPTAINER_IMAGE_PATH="/sdf/scratch/users/s/sanjeev/singularity/impact-bmad_latest.sif"

apptainer overlay create --size 10000 --fakeroot ${APPTAINER_IMAGE_PATH}



===========================


working




#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=FACET
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=01:00:00
#SBATCH --pty /bin/bash

# Load necessary modules
#module load singularity

# Define the path to your Singularity image
APPTAINER_IMAGE_PATH="/sdf/scratch/users/s/sanjeev/singularity/impact-bmad_latest.sif"

function jupyter() {
    SCRATCH_PATH=$(echo $SCRATCH)
    apptainer exec  -B /sdf,/fs,/sdf/scratch,/lscratch --env SCRATCH=$SCRATCH_PATH ${APPTAINER_IMAGE_PATH} jupyter lab --no-browser --allow-root --notebook-dir=/opt/notebooks --port=5555 "$@"
}


jupyter

===========