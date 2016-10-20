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

def replace(dic, keys,value):
    getValue(dic,keys[:-1])[keys[-1]]=value

def getValue(dic, keys):
    return reduce(lambda d, k: d[k], keys, dic)

def search_list(value,keys):
    if not isinstance(value,list):
        for key,val in value.iteritems():
            keys.append(key)
            keys,value = search_list(val,keys)
    
    return keys, value


keys,values = search_list(search.params,[])

for value in values:

    replace(external.params,keys,value)

    Populations = h.build_network(external.params)

    cells = Populations['py'].local_cells
    cells = cells[0:int(0.2*len(cells))]
    for cell in cells:
        cell.a = 0.02e3
        cell.b = 0.0

    
    h.record_data(external.params, Populations)

    h.run_simulation(external.params)
    
    h.save_data(Populations,addon=keys[-1]+str(value))

    end()

    h.analyse(Populations,keys[-1]+str(value))
