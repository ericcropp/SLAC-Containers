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


# Set environment variables
ENV CONDA_AUTO_UPDATE_CONDA=false

# Install SSL dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set architecture
RUN conda config --set subdir linux-64


# Configure conda channels and set architecture
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict 
# Update conda and install lume-impact
RUN conda update -n base -c defaults conda && \
    conda install conda-forge::lume-impact -y --solver classic


#RUN /opt/conda/bin/conda install conda-forge::lume-impact -y
RUN  sed -i "s|workdir = full_path(workdir)|workdir = tools.full_path(workdir) |g" /opt/conda/lib/python3.12/site-packages/lume/base.py


RUN conda search impact-t --channel conda-forge
RUN /opt/conda/bin/conda install -c conda-forge impact-t
RUN /opt/conda/bin/conda install -c conda-forge impact-t=*=mpi_openmpi*

RUN /opt/conda/bin/conda install jupyter
RUN /opt/conda/bin/conda install jupyterlab


RUN /opt/conda/bin/conda install scipy
RUN /opt/conda/bin/conda install numpy
RUN /opt/conda/bin/conda install matplotlib
RUN /opt/conda/bin/conda install pillow
RUN /opt/conda/bin/conda install pandas
RUN /opt/conda/bin/conda install conda-forge::xopt

RUN /opt/conda/bin/conda install conda-forge::distgen
RUN /opt/conda/bin/conda install h5py
RUN /opt/conda/bin/conda install conda-forge::openpmd-beamphysics
# ------------------------------------------------------------
# Copy Jupyter notebooks into the image
# ------------------------------------------------------------

COPY notebooks /opt/notebooks

# Expose port for JupyterLab
EXPOSE 8888

# Default command to run JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--notebook-dir=/opt/notebooks"]
