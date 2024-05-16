# Base image
FROM ubuntu:latest

# Set working directory
WORKDIR /opt

# Install necessary packages and MPICH
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        gfortran \
        python3-dev \
        python3-pip \
        wget && \
    apt-get clean && \
    wget https://www.mpich.org/static/downloads/4.0.2/mpich-4.0.2.tar.gz && \
    tar xvzf mpich-4.0.2.tar.gz && \
    cd mpich-4.0.2 && \
    ./configure && \
    make -j 4 && \
    make install && \
    make clean && \
    cd .. && \
    rm -rf mpich-4.0.2 && \
    rm mpich-4.0.2.tar.gz && \
    ldconfig && \
    python3 -m pip install mpi4py

# Use Miniconda base image
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PATH=/opt/conda/bin:$PATH

# Ensure conda has proper permissions
RUN chmod -R 777 /opt/conda

# Install necessary conda packages
RUN /opt/conda/bin/conda install -y \
    conda-forge::lume-impact \
    impact-t \
    impact-t=*=mpi_openmpi* \
    jupyter \
    jupyterlab \
    scipy \
    numpy \
    matplotlib \
    pillow \
    pandas \
    conda-forge::xopt \
    conda-forge::distgen \
    h5py \
    conda-forge::openpmd-beamphysics \
    pytao \
    pmd_beamphysics \
    pyyaml \
    pickle && \
    sed -i "s|workdir = full_path(workdir)|workdir = tools.full_path(workdir)|g" /opt/conda/lib/python3.12/site-packages/lume/base.py

# Expose port for JupyterLab
EXPOSE 8888

# copy over notebooks and helper files
COPY . /opt/

# Default command to run JupyterLab
CMD ["/opt/conda/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
