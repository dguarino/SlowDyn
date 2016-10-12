import NeuroTools.signals
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt
import helpers as h
import params as p

#usage_str = 'usage: run.py -p <param file>'

#try:
#      opts, args = getopt.getopt(sys.argv[1:], "hp:" )
#except getopt.GetoptError:
#    print usage_str,"error"
#    sys.exit(2)
#if len(opts)==0:
#    print usage_str,"empty opts"
#for opt, arg in opts:
#    if opt == '-h':
#        print usage_str
#        sys.exit()
#    elif opt == '-p':
#        params = __import__(arg)

Populations = h.build_network(p.Params)

h.record_data(p.Params,Populations)

h.run_simulation(p.Params)

h.save_data(Populations)

end()
