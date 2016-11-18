import NeuroTools.signals
import numpy.random
import os
import csv
import shutil
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt
import itertools as it

import helpers as h


# ADDITIONAL FUNCTIONS ---------------------------------------------------------
def replace(dic, keys,value):
    getValue(dic,keys[:-1])[keys[-1]]=value

def getValue(dic, keys):
    return reduce(lambda d, k: d[k], keys, dic)



# ------------------------------------------------------------------------------
usage_str = 'usage: run.py [-a] [-r] -p<param file> -f<data folder> [-s<search file>]'
doAnalaysisOnly = False
doParameterSearch = False
removeDataFile = False
data_folder = 'results'
params_filename = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], "harf:p:s:" )
except getopt.GetoptError:
    print usage_str,"error"
    sys.exit(2)
if len(opts)==0:
    print usage_str,"empty opts"
for opt, arg in opts:
    if opt == '-h':
        print usage_str
        sys.exit()
    elif opt == '-a':
        print "Running analysis and plotting only ..."
        doAnalaysisOnly=True
    elif opt == '-r':
        print "Removing data files after analysis ..."
        removeDataFile=True
    elif opt == '-f':
        data_folder = arg
        print "Data will be saved in:", data_folder
    elif opt == '-p':
        print "Using parameter file:", arg
        external = __import__(arg)
        params_filename = arg
    elif opt == '-s':
        print "Executing parameter search using file:", arg
        search = __import__(arg)
        doParameterSearch = True

if params_filename=='':
    print usage_str,"error"
    sys.exit(2)


combinations = [{'default':''}] # init
if doParameterSearch:
    # create parameter combinations
    testParams = sorted(search.params) # give an order to dict (by default unordered)

    # create an array of dictionaries:
    # each dict being the joining of one of the testKey and a value testVal
    # each testVal is produced by internal product of all array in testParams
    combinations = [dict(zip(testParams, testVal)) for testVal in it.product(*(search.params[testKey] for testKey in testParams))]
    #print len(combinations),combinations # to be commented

    with open(data_folder+'/map.csv', 'w') as csvfile:
        mywriter = csv.writer(csvfile)
        mywriter.writerow( ['#'+str(testParams[0])+ ':' +str(search.params[testParams[0]]) ] )
        mywriter.writerow( ['#'+str(testParams[1])+ ':' +str(search.params[testParams[1]]) ] )

info = []
print 'info',info
# run combinations
for i,comb in enumerate(combinations):
    print "param combination",i
    print "current set:",comb

    # replacement
    for ckey,val in comb.iteritems():
        keys = ckey.split('.') # get list from dotted string
        replace(external.params,keys,val)

    # save parameters in the data_folder
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    shutil.copy('./'+params_filename+'.py', data_folder+'/'+params_filename+'_'+str(comb)+'.py')

    if not doAnalaysisOnly:
        Populations = h.build_network(external.params)
        h.record_data(external.params, Populations)
        h.perform_injections(external.params, Populations)
        h.run_simulation(external.params)
        h.save_data(Populations, data_folder, str(comb))
        end()

    else:
        ratio,fqcy = h.analyse(external.params, data_folder, str(comb), removeDataFile)
        info.append([ratio,fqcy])
        if (i+1)%len(search.params[testParams[1]]) == 0:
            with open(data_folder+'/map.csv', 'a') as csvfile:
                mywriter = csv.writer(csvfile)
                mywriter.writerow(info)
            info = []

        #write (fqcy,ratio) to map.csv file in which each row is an "a" value and each column is a "b" value + first 2 lines commented with values of a and b
