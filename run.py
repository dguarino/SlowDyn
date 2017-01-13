"""
Copyright (c) 2016, Domenico GUARINO, Eloise SOULIER
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL GUARINO AND SOULIER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import NeuroTools.signals
import os
import csv
import shutil
from pyNN.utility import get_simulator
from pyNN.utility import init_logging
from pyNN.utility import normalized_filename
from pyNN.utility import Timer
import numpy as np
import matplotlib.pyplot as plot
import sys, getopt
import itertools as it

import helpers as h




# ADDITIONAL FUNCTIONS ---------------------------------------------------------

def replace(dic, keys,value):
    getValue(dic,keys[:-1])[keys[-1]]=value

def getValue(dic, keys):
    return reduce(lambda d, k: d[k], keys, dic)


sim, opts = get_simulator(
        ("--analysis", "Perform analysis only", {"type":bool}),
        ("--remove", "Remove data files (after analysis)", {"type":bool}),
        ("--folder", "Folder to save the data in (created if it does not exists)", {"dest":"data_folder", "required":True}),
        ("--params", "Parameter filename", {"dest":"param_file", "required":True}),
        ("--search", "Parameter search filename", {"dest":"search_file"}),
        ("--map",    "Produce a map of 2D parameter search", {"type":bool}),
        ("--debug", "Print debugging information")
    )

if opts.debug:
    init_logging(None, debug=True)

if opts.analysis:
    print "Running analysis and plotting only ..."

if opts.remove:
    print "Removing data files after analysis ..."

if opts.data_folder:
    print "Data will be saved in:", opts.data_folder

params = {}
if opts.param_file != '':
    print "Using parameter file:", opts.param_file
    with open(opts.param_file, 'r') as pfile:
        pstring = pfile.read()
        params = eval(pstring)
else:
    print "ERROR: you must specify a parameter file!"
    sys.exit(2)

search = {}
if opts.search_file:
    print "Executing parameter search using file:", opts.search_file
    with open(opts.search_file, 'r') as sfile:
        sstring = sfile.read()
        search = eval(sstring)



# ------------------------------------------------------------------------------

#usage_str = 'usage: run.py [-a] [-r] -f<data folder> -p<param file> [-s<search file>]'
#doAnalysisOnly = False
#doParameterSearch = False
#removeDataFile = False
#data_folder = 'results'
#params_filename = ''

#try:
#    opts, args = getopt.getopt(sys.argv[1:], "harf:p:s:" )
#    print opts,args
#except getopt.GetoptError:
#    print usage_str,"error"
#    sys.exit(2)
#if len(opts)==0:
#    print usage_str,"empty opts"
#for opt, arg in opts:
#    if opt == '-h':
#         print usage_str
#        sys.exit()
#    elif opt == '-a':
#        print "Running analysis and plotting only ..."
#        doAnalysisOnly=True
#    elif opt == '-r':
#        print "Removing data files after analysis ..."
#        removeDataFile=True
#    elif opt == '-f':
#        data_folder = arg
#        print "Data will be saved in:", data_folder
#    elif opt == '-p':
#        print "Using parameter file:", arg
#        external = __import__(arg)
#        params_filename = arg
#    elif opt == '-s':
#        print "Executing parameter search using file:", arg
#        search = __import__(arg)
#        doParameterSearch = True
        
#if params_filename=='':
#    print usage_str,"error"
#    sys.exit(2)

combinations = [{'default':''}] # init
if search:
    # create parameter combinations
    testParams = sorted(search) # give an order to dict (by default unordered)
    # create an array of dictionaries:
    # each dict being the joining of one of the testKey and a value testVal
    # each testVal is produced by internal product of all array in testParams
    combinations = [dict(zip(testParams, testVal)) for testVal in it.product(*(search[testKey] for testKey in testParams))]
    #print len(combinations),combinations # to be commented

for run in range(params['nb_runs']):
    info = []
    # run combinations
    for i,comb in enumerate(combinations):
        print "param combination",i, "trial",run
        print "current set:",comb

        # replacement
        for ckey,val in comb.iteritems():
            keys = ckey.split('.') # get list from dotted string
            replace(params,keys,val)

        # save parameters in the data_folder
        if not os.path.exists(opts.data_folder+str(run)):
            os.makedirs(opts.data_folder+str(run))
        shutil.copy('./'+opts.param_file, opts.data_folder+ str(run)+'/'+opts.param_file+'_'+str(comb)+'.py')

        if not opts.analysis:
            already_computed = 0
            for pop in params['Populations'].keys():
                if os.path.exists(opts.data_folder + str(run) +'/'+pop+str(comb)+'.pkl'):
                    already_computed = already_computed + 1
            if already_computed > 0:
                print "already computed"
            else:
                Populations = h.build_network(sim,params)
                h.record_data(params, Populations)
                h.perform_injections(params, Populations)
                h.run_simulation(sim,params)
                h.save_data(Populations, opts.data_folder + str(run), str(comb))
                sim.end()
        else :
            if search:
                already_computed = 0
                for pop in params['Populations'].keys():
                    if os.path.exists(opts.data_folder + str(run) +'/'+pop+str(comb)+'.png'):
                        already_computed = already_computed + 1
                if already_computed > len(params['Populations']) - 1:
                    print "already analysed"
                else:
                    ratio,fqcy,psd,freq, fqcy_ratio = h.analyse(params, opts.data_folder + str(run), str(comb), removeDataFile)
                    print "ratio",ratio,"fqcy",fqcy,"psd",psd,"freq",freq
                    
                    gen = (pop for pop in params['Populations'].keys() if pop != 'ext')
                    for pop in gen:
                        if i == 0:
                            with open(opts.data_folder+ str(run)+'/map-'+pop+'.csv', 'wb') as csvfile:
                                mywriter = csv.writer(csvfile)
                                mywriter.writerow( ['#'+str(testParams[1])+ ':' +str(search[testParams[1]]) ] )
                                mywriter.writerow( ['#'+str(testParams[0])+ ':' +str(search[testParams[0]]) ] )

                            with open(opts.data_folder+ str(run)+'/psdmap-'+pop+'.csv', 'wb') as csvfile:
                                mywriter = csv.writer(csvfile)
                                mywriter.writerow( ['#'+str(testParams[1])+ ':' +str(search[testParams[1]]) ] )
                                mywriter.writerow( ['#'+str(testParams[0])+ ':' +str(search[testParams[0]]) ] )
                                if pop in freq:
                                    mywriter.writerow(freq[pop])

                        if pop in ratio and pop in fqcy:
                            print "appending to map",ratio,fqcy
                            info.append([ratio[pop],fqcy[pop],fqcy_ratio[pop]])
                            if (i+1)%len(search[testParams[1]]) == 0:
                                with open(opts.data_folder+str(run)+'/map-'+pop+'.csv', 'a') as csvfile:
                                    mywriter = csv.writer(csvfile)
                                    mywriter.writerow(info)
                                    info = []
                        if pop in psd:
                            with open(opts.data_folder+str(run)+'/psdmap-'+pop+'.csv', 'a') as csvfile:
                                mywriter = csv.writer(csvfile)
                                mywriter.writerow(psd[pop])

            else:
                h.analyse(params, opts.data_folder+str(run), str(comb), removeDataFile)
                info = []



                #if doAnalaysisOnly:
#    with open(data_folder+'/map.csv', 'a') as csvfile:
#        h.plot_map(csvfile, factor)
