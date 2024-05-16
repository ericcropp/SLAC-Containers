# Base image
FROM ubuntu:latest

# Set working directory
WORKDIR /opt

# Install necessary packages and MPICH
RUN apt-get update && \
    apt-get install --yes \
        build-essential \
        gfortran \
        python3-dev \
        python3-pip \
        wget && \
    apt-get clean all

ARG mpich=4.0.2
ARG mpich_prefix=mpich-$mpich

RUN wget https://www.mpich.org/static/downloads/$mpich/$mpich_prefix.tar.gz && \
    tar xvzf $mpich_prefix.tar.gz && \
    cd $mpich_prefix && \
    ./configure && \
    make -j 4 && \
    make install && \
    make clean && \
    cd .. && \
    rm -rf $mpich_prefix

RUN /sbin/ldconfig

RUN python3 -m pip install mpi4py

# Use Miniconda base image
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PATH=/opt/conda/bin:$PATH

# Ensure conda has proper permissions
RUN chmod -R 777 /opt/conda

# Configure conda channels
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict

# Update conda to the latest version
RUN conda update -n base -c defaults conda -y

# Install Lume-Impact and fix the path in lume/base.py
RUN conda install -y lume-impact && \
    sed -i "s|workdir = full_path(workdir)|workdir = tools.full_path(workdir)|g" /opt/conda/lib/python3.12/site-packages/lume/base.py

# Install Impact-T with MPICH
RUN  conda search impact-t --channel conda-forge    
#RUN conda install -c conda-forge "impact-t=*=mpi_mpich*" --verbose -y

# Install additional packages
RUN conda install -y jupyter jupyterlab scipy numpy matplotlib pillow pandas xopt distgen h5py openpmd-beamphysics pytao pmd_beamphysics pyyaml pickle

# Copy Jupyter notebooks into the image
COPY notebooks /opt/notebooks

# Expose port for JupyterLab
EXPOSE 8888

# Default command to run JupyterLab
CMD ["/opt/conda/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--notebook-dir=/opt/notebooks"]
