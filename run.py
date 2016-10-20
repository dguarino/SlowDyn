import NeuroTools.signals
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt

import helpers as h

usage_str = 'usage: run.py -p <param file> -s <search file>'

try:
      opts, args = getopt.getopt(sys.argv[1:], "hp:s:" )
except getopt.GetoptError:
    print usage_str,"error"
    sys.exit(2)
if len(opts)==0:
    print usage_str,"empty opts"
for opt, arg in opts:
    if opt == '-h':
        print usage_str
        sys.exit()
    elif opt == '-p':
        print arg
        external = __import__(arg)
    elif opt == '-s':
        print arg
        search = __import__(arg)

Populations = h.build_network(external.params)

h.record_data(external.params, Populations)

h.run_simulation(external.params)

h.save_data(Populations)


end()

h.analyse(Populations,'')
