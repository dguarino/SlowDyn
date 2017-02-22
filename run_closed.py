import NeuroTools.signals
import numpy as np
import os
import csv
import shutil
import matplotlib.pyplot as plot
from pyNN.utility import get_simulator
from pyNN.utility import init_logging
from pyNN.utility import normalized_filename
from pyNN.utility import Timer
from joblib import Parallel,delayed
from functools import partial
import sys, getopt
import itertools as it

import helpers as h


# ADDITIONAL FUNCTIONS ---------------------------------------------------------
def replace(dic, keys,value):
    getValue(dic,keys[:-1])[keys[-1]]=value

def getValue(dic, keys):
    return reduce(lambda d, k: d[k], keys, dic)


#STIMULATION FUNCTIONS ---------------------------------------------------------

def inject_spikes_pop(t,Populations):
    if t>0.0:
        data = Populations['py'].get_data().segments[0]
        lfp = compute_lfp(data,params['push_interval'],t,params['dt'])
        #spike_times = open_loop(t,lfp)
	spike_times = closed_loop(t,lfp)
	params['spike_times'] = params['spike_times'] + spike_times
        Populations['audio'].set(spike_times=spike_times)
    return t + 5. #params['push_interval']



def closed_loop(t, eeg):
    # use the eeg interval (N ms) to compute the input
    #threshold = 0.
    signal = eeg #- threshold
    threshold_crossing =  signal[1:]* signal[0:-1]  < 0
    #stimulate if threshold crossing is positive
    stim = False
    spike_times = []
    for index in range(1,len(threshold_crossing)-1):
	if threshold_crossing[index] and (signal[index] - signal[index-1])>0:
            stim = True
    if stim == True:
	spike_times = [t+1+i for i in range(params['nb_push'])]
    return spike_times


def open_loop(t, eeg):
    #open loop stimulation
    spike_times = [t+1+i for i in range(params['nb_push'])]

    return spike_times	


def compute_lfp(data,interval,t,dt):
    v = data.filter(name="v")[0][(t-interval)/dt:t/dt]
    g_exc = data.filter(name="gsyn_exc")[0][(t-interval)/dt:t/dt]
    g_inh = data.filter(name="gsyn_inh")[0][(t-interval)/dt:t/dt]
    i = (g_exc+g_inh)*v
    avg_i_by_t = np.sum(i,axis=0)/i.shape[0] # / time steps
    sigma = 0.1 # [0.1, 0.01] # value from Dobiszewski_et_al2012.pdf
    lfp = (1/(4*np.pi*sigma)) * avg_i_by_t 
    return lfp
 


            
def report_time(t):
     print "The time is %g" % t
     return t + 100.0


# ----------------
# one external input source is a spike array
# stimulus = sim.Population(1, sim.SpikeSourceArray(spike_times=spike_times), label="Input spikes")



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

#opts.analysis = True #uncomment for analysis if command line setting doesn't work


combinations = [{'default':''}] # init
if search:
    # create parameter combinations
    testParams = sorted(search) # give an order to dict (by default unordered)
    # create an array of dictionaries:
    # each dict being the joining of one of the testKey and a value testVal
    # each testVal is produced by internal product of all array in testParams
    combinations = [dict(zip(testParams, testVal)) for testVal in it.product(*(search[testKey] for testKey in testParams))]



def run_simulation(run):

    info = {}
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
        shutil.copy('./'+opts.param_file, opts.data_folder + str(run)+'/'+opts.param_file+'_'+str(comb)+'.py')

        if not opts.analysis: #run simulation
	    # run simulation if it hasn't already been ran for these parameters
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
                print "Running Network"
                timer = Timer()
                timer.reset()
		inject_spikes = partial(inject_spikes_pop,Populations = Populations)
                sim.run(params['run_time'], [inject_spikes])
                simCPUtime = timer.elapsedTime()
                print "Simulation Time: %s" % str(simCPUtime)
                h.save_data(Populations, opts.data_folder + str(run), str(comb))
                sim.end()

        else : #do analysis
            if search: #then compute the csv needed for the search maps
                already_analysed = 0 #analyse only those that haven't already been analysed
                for pop in params['Populations'].keys():
                    if os.path.exists(opts.data_folder + str(run) +'/'+pop+str(comb)+'.png'):
                        already_analysed = already_analysed + 1
                if already_analysed >= len(params['Populations'])-1 :
                    print "already analysed"
                else:	
                    ratio,fqcy,psd,freq, fqcy_ratio = h.analyse(params, opts.data_folder + str(run), str(comb), opts.remove)
 		    #save computed values in csv files                   
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
			    info[pop] = []

                        if pop in ratio and pop in fqcy:
                            info[pop].append([ratio[pop],fqcy[pop],fqcy_ratio[pop]])
                            if (i+1)%len(search[testParams[1]]) == 0:
                                with open(opts.data_folder+str(run)+'/map-'+pop+'.csv', 'a') as csvfile:
                                    mywriter = csv.writer(csvfile)
                                    mywriter.writerow(info[pop])
                                    info[pop] = []
                        if pop in psd:
                            with open(opts.data_folder+str(run)+'/psdmap-'+pop+'.csv', 'a') as csvfile:
                                mywriter = csv.writer(csvfile)
                                mywriter.writerow(psd[pop])

            else:
                h.analyse(params, opts.data_folder+str(run), str(comb), opts.remove)
                




for run in range(params['nb_runs']):
    run_simulation(run)

#Uncomment these lines to parallelize and comment the previous ones

#Parallel(n_jobs=6)(delayed(run_simulation)(run) for run in range(params['nb_runs']))
#h.run_simulation(external.params)


sim.end()
