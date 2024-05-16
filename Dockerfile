# Base image
FROM ubuntu:18.04

# Set working directory
WORKDIR /opt

# Install necessary packages and OpenMPI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        python3-dev \
        python3-pip \
        wget \
        openmpi-bin \
        libopenmpi-dev \
        libssl-dev \
        libcrypto++-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install mpi4py with pip
RUN python3 -m pip install mpi4py

# Use Miniconda base image
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PATH=/opt/conda/bin:$PATH

# Ensure conda has proper permissions
RUN chmod -R 777 /opt/conda

# Configure conda channels and set architecture
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda config --set subdir linux-64

# Update conda to the latest version and use the classic solver
RUN conda update -n base -c defaults conda -y && \
    conda config --set solver classic

# Create a new conda environment named 'simulation' and install packages
RUN conda create -n simulation -y && \
    CONDA_NO_PLUGINS=true conda install -n simulation -c conda-forge impact-t=2.3.1=mpi_openmpi_hce253eb_0 && \
    CONDA_NO_PLUGINS=true conda install -n simulation -y lume-impact jupyter jupyterlab scipy numpy matplotlib pillow pandas xopt distgen h5py openpmd-beamphysics pytao pmd_beamphysics pyyaml pickle

# Fix the path in lume/base.py within the 'simulation' environment
RUN sed -i "s|workdir = full_path(workdir)|workdir = tools.full_path(workdir)|g" /opt/conda/envs/simulation/lib/python3.12/site-packages/lume/base.py

# Set environment variables to activate the 'simulation' environment by default
ENV CONDA_DEFAULT_ENV=simulation
ENV PATH=/opt/conda/envs/simulation/bin:$PATH
RUN echo "source activate simulation" > ~/.bashrc



# ------------------------------------------------------------
# Copy Jupyter notebooks into the image
# ------------------------------------------------------------

COPY notebooks /opt/notebooks

# Expose port for JupyterLab
EXPOSE 8888

# Default command to run JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--notebook-dir=/opt/notebooks"]
