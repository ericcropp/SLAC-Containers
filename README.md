
# FACET2 Injector Simulation Docker Image

## Overview
This repository contains the necessary components to create a Docker image that encapsulates a Jupyter Notebook simulation environment for the FACET2 injector. Github actions automatically builds the container and updates the local copy on S3DF. The simulation utilizes both IMPACT and BMAD codes to model and analyze the injector's behavior. The juptyer notebooks are written by [Eric Cropp](https://github.com/ericcropp/Impact-T_Examples/blob/main/FACET-II_Impact_Bmad/Impact_Bmad.ipynb). Additionally, the repository includes a script to facilitate running the Docker container on the S3DF platform.

## Docker Image
The Docker image is designed to provide a ready-to-use simulation environment with pre-installed dependencies and configurations necessary for running IMPACT and BMAD simulations. The core of this environment is a Jupyter Notebook that guides users through the simulation process, from setting up initial conditions to visualizing the results.

### Components
- **Jupyter Notebook**: Contains the simulation workflow, including setup, execution, and analysis steps.
- **IMPACT**: A particle accelerator simulation tool used for the initial stages of the simulation.
- **BMAD**: A library for simulating charged particle beams and designing accelerators, used in the latter stages of the simulation.

## Running the Container on S3DF
Included in this repository is a script that simplifies the process of deploying and running the Docker container on the S3DF platform. This script handles copying the notebooks to a working directory on s3df and runs a local copy of the container on s3df.

### Usage
To run the Docker container on S3DF, execute the provided script with the necessary parameters. Instructions are on confluence ([here](https://confluence.slac.stanford.edu/x/HAGHGw))


## Support
For any issues or questions regarding the setup, execution, or other aspects of using this Docker image, please refer to the documentation provided [[here](https://confluence.slac.stanford.edu/x/HAGHGw)] or contact sanjeev@slac.stanford.edu.
