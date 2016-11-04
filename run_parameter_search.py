import NeuroTools.signals
import numpy.random
import numpy as np
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt

import helpers as h
import itertools as it


def replace(dic, keys,value):
    getValue(dic,keys[:-1])[keys[-1]]=value

def getValue(dic, keys):
    return reduce(lambda d, k: d[k], keys, dic)



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


# create parameter combinations
testParams = sorted(search.params) # give an order to dict (by default unordered)
# create an array of dictionaries:
# each dict being the joining of one of the testKey and a value testVal
# each testVal is produced by internal product of all array in testParams
combinations = [dict(zip(testParams, testVal)) for testVal in it.product(*(search.params[testKey] for testKey in testParams))]
print len(combinations),combinations # to be commented

score = {}
# run combinations
for i,comb in enumerate(combinations):
    print "param combination",i
    print "current set:",comb

    # replacement
    for ckey,val in comb.iteritems():
        keys = ckey.split('.') # get list from dotted string
        #print "before:", getValue(external.params, keys)
        replace(external.params,keys,val)
        #print "after:", getValue(external.params, keys)

    Populations = h.build_network(external.params)
    print Populations
    #print 'dopo fuori:',getattr(Populations['py'][7], 'a')

    h.record_data(external.params, Populations)

    h.run_simulation(external.params)
    
    h.save_data(Populations,addon=str(comb))
    
    score_local = h.analyse(Populations,str(comb))
    score[str(comb)] = score_local
    

    end()

#for key in Populations:
#    max = np.max(score.values())
#    print score.keys()[score.values().index(max)]
target = open('score.txt', 'a')
target.write(str(score))
