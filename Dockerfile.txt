FROM ubuntu:latest
WORKDIR /opt

RUN \
    apt-get update        && \
    apt-get install --yes    \
        build-essential      \
        gfortran             \
        python3-dev          \
        python3-pip          \
        wget              && \
    apt-get clean all

ARG mpich=4.0.2
ARG mpich_prefix=mpich-$mpich

RUN \
    wget https://www.mpich.org/static/downloads/$mpich/$mpich_prefix.tar.gz && \
    tar xvzf $mpich_prefix.tar.gz                                           && \
    cd $mpich_prefix                                                        && \
    ./configure                                                             && \
    make -j 4                                                               && \
    make install                                                            && \
    make clean                                                              && \
    cd ..                                                                   && \
    rm -rf $mpich_prefix

RUN /sbin/ldconfig

RUN python3 -m pip install mpi4py


FROM docker.io/continuumio/miniconda3:latest

ENV PATH=/opt/conda/bin:$PATH

RUN chmod -R 777 /opt/conda

RUN /opt/conda/bin/conda install conda-forge::lume-impact
RUN  sed -i "s|workdir = full_path(workdir)|workdir = tools.full_path(workdir) |g" /opt/conda/lib/python3.12/site-packages/lume/base.py

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