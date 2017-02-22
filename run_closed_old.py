import NeuroTools.signals
import numpy as np
import os
import csv
import shutil
from pyNN.utility import get_simulator
from pyNN.utility import init_logging
from pyNN.utility import normalized_filename
from pyNN.utility import Timer
import numpy as np
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


class SetInput(object):
    """
    """

    def __init__(self, populations, interval=20.0, dt=0.1):
	print "initiated"
        self.interval = interval
        self.populations = populations
        self.dt = dt

    def closed_loop(self, t, eeg):
        # use the eeg interval (N ms) to compute the input

        ## Proposta di struttura 
        threshold = somevalue
        #is the threshold crossed ?
        signal = eeg - threshold
        threshold_crossing =  signal[1:]* signal[0:-1]  < 0
        #stimulate if threshold crossing is positive
        for index in range(1,len(threshold_crossing)-1):
            if threshold_crossing[index] and (signal[index] - signal[index-1])>0:
                stim = true
                spike_times = [index+1]#, t+3, t+4] # result of the rythm_func
            else: 
                spike_times = 0
        return spike_times
    
    def open_loop(self, t, eeg):
        print "inside open_loop"
        if t % 1000 == 0:
            spike_times = [t+1,t+2,t+3]
        else:
            spike_times = 0

        return spike_times

    def __call__(self, t):
        print "called"
        try:
            lfp = 0.0
            if t>0.0: # there needs to be data, so after time 0 :)
                data = self.populations['py'].get_data().segments[0]
                # get only the last interval recordings
                # during an interval (10ms) (101, 10)
                # we are recording for 10ms*0.1ms dt = 101, from 10 cells
                v = data.filter(name="v")[0][(t-self.interval)*self.interval:t*self.interval]
                g = data.filter(name="gsyn_exc")[0][(t-self.interval)*self.interval:t*self.interval]
                #print t, 'v', v.shape
                #print t, 'g', g.shape
                # We produce the current for each cell for this time interval, with the Ohm law:
                # I = g(V-E), where E is the equilibrium for exc which is usually 0.0 (we can change it)
                # (and we also have to consider inhibitory condictances)
                i = g*(v)
                print "computing lfp"
                #print 'i',i.shape
                #print i
                # http://www.scholarpedia.org/article/Local_field_potential
                # the LFP is the result of all cells' currents
                avg_i_by_t = numpy.sum(i,axis=0)/i.shape[0] # / time steps
                #print avg_i_by_t.shape
                #print avg_i_by_t
                sigma = 0.1 # [0.1, 0.01] # Dobiszewski_et_al2012.pdf
                lfp = (1/(4*numpy.pi*sigma)) * avg_i_by_t 
                # a very large LFP would give us a signal comparable to eeg
                # - https://www.quora.com/Neuroscience-What-is-difference-between-local-field-potential-and-EEG
                # - Musall et al 2012
                # - Bartosz (personal communication)
                print lfp
            # LFP into rythm_func
            spike_times = self.open_loop(t,lfp)
            self.populations['audio'].set(spike_times=spike_times)
        except StopIteration:
            pass
        return t + self.interval

            
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

opts.analysis = True


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
                print "Running Network"
                timer = Timer()
                timer.reset()
                interval = 10
                sim.run(params['run_time'], callbacks = SetInput(Populations, interval, params['dt']))
                simCPUtime = timer.elapsedTime()
                print "Simulation Time: %s" % str(simCPUtime)
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
                    ratio,fqcy,psd,freq, fqcy_ratio = h.analyse(params, opts.data_folder + str(run), str(comb), opts.remove)
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





#h.run_simulation(external.params)


sim.end()
