# SlowDyn
Cortical network simulation for slow wave oscillation.

This file implements a PyNN version of the model detailed in Destexhe, "A. Self-sustained asynchronous irregular states and Up/Down states in thalamic, cortical and thalamocortical networks of nonlinear integrate-and-fire neurons" (Journal of Computational Neuroscience 27: 493-506, 2009).

## Installation of NEST and pyNN

###1. Create a virtualenv
with either virtualenv, virtualenwrapper, or conda.

In the reminder of this text we will use the name 'pynn' for our virtualenv.

###2. Install pyNN
> (pynn)$ pip install pyNN


###3. Download the latest version of NEST that is compatible with PyNN
- Compatibility: http://neuralensemble.org/docs/PyNN/installation.html#installing-nest-and-pynest
- Versions of NEST: http://www.nest-simulator.org/download/


###4. Prerequisites for NEST
Install the following packages (they will be installed system-wide):
> $ sudo apt-get install build-essential autoconf automake libtool libltdl7-dev libreadline6-dev libncurses5-dev libgsl0-dev python-all-dev python-numpy python-scipy python-matplotlib ipython

> $ sudo apt-get install openmpi-bin openmpi-common libopenmpi-dev


###5. Install NEST
Follow the instructions at http://www.nest-simulator.org/installation/
> $ tar -xvf nest-2.10.0.tar.gz
> $ cd nest-2.10.0/
> $ ./configure --with-mpi  --prefix=$HOME/opt/nest
> $ sudo make
> $ sudo make install
> $ sudo make installcheck

###6. Tell bash how to find NEST
> $ vi .bashrc

and add the following lines at the end of the file:
~~~~
export PATH=$PATH:$HOME/opt/nest/bin
export PYTHONPATH=$HOME/opt/nest/lib/python2.7/site-packages:$PYTHONPATH
~~~~

###7. fast test
> $ python

~~~~
>>> import nest
-- N E S T --

Copyright (C) 2004 The NEST Initiative
Version 2.10.0 Jun 24 2016 13:15:45

This program is provided AS IS and comes with
NO WARRANTY. See the file LICENSE for details.

Problems or suggestions?
Visit http://www.nest-simulator.org

Type 'nest.help()' to find out more about NEST.
>>>
~~~~

###8. Tell NEST how to use mpi
> $ vi .nestrc

and uncomment the command mpirun at the beginning of nestrc

###9. Add the requirements for scipy
> $ sudo apt-get install libblas-dev libblas-doc libblas3 liblapack-dev liblapack-doc liblapack3 liblapacke liblapacke-dev

###10. Add requirements for matplotlib
> $ sudo apt-get install libfreetype6 libfreetype6-dev libpng12-0 libpng12-dev

###11. Add the requirements for pyNN
from the file requirements.txt, usually:
~~~~
ConnPlotter==0.7a0  #comes with NEST
lazyarray==0.2.8
neo==0.3.3
numpy==1.11.0
PyNEST==2.10.0   #comes with NEST
PyNN==0.8.1
quantities==0+unknown
Topology==2.10.0     #comes with NEST
wheel==0.24.0
~~~~
