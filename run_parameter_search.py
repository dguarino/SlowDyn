import NeuroTools.signals
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt

import helpers as h
import itertools as it


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

# http://stackoverflow.com/questions/3873654/combinations-from-dictionary-with-list-values-using-python
varNames = sorted(search.params)
combinations = [dict(zip(varNames, prod)) for prod in it.product(*(search.params[varName] for varName in varNames))]
#print len(combinations),combinations

for i,comb in enumerate(combinations):
    print "param combination",i
    print "current set:",comb

    # replacement
    for ckey,val in comb.iteritems():
        keys = ckey.split('.') # get list from dotted string
        external.params[keys[-1]] = val # this is what i did not remember

    Populations = h.build_network(external.params)

    h.record_data(external.params, Populations)

    h.run_simulation(external.params)

    h.save_data(Populations,addon=str(value))

    end()

    h.analyse(Populations,str(value))
