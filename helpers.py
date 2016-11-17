import NeuroTools.signals
import numpy as np
import random as rd
import os
import scipy.io
from scipy.fftpack import fft
from scipy import signal
from pyNN.nest import *
from pyNN.utility import Timer
import pickle
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plot
from datetime import datetime


def build_network(Params):
    setup( timestep=Params['dt'])

    Populations = {}
    for popKey,popVal in Params['Populations'].iteritems():
        if isinstance(popVal['n'],dict):
            number = int(Params['Populations'][popVal['n']['ref']]['n'] * popVal['n']['ratio'])
            Populations[popKey] = Population( number, popVal['type'], cellparams=popVal['cellparams'] )
        else:
            Populations[popKey] = Population( popVal['n'], popVal['type'], cellparams=popVal['cellparams'] )

    Projections = {}
    for projKey,projVal in Params['Projections'].iteritems():
        Projections[projKey] = Projection(
            Populations[ projVal['source'] ],
            Populations[ projVal['target'] ],
            connector = projVal['connector'],
            synapse_type = projVal['synapse_type'](weight = projVal['weight']),
            receptor_type = projVal['receptor_type']
        )


    for key in Populations.keys():
        Populations[key].initialize()

    for modKey,modVal in Params['Modifiers'].iteritems():
        if type(modVal['cells']['start']) == float:
            start = int(modVal['cells']['start'] * Populations[modKey].local_size)
        else:
            start = modVal['cells']['start']
        if type(modVal['cells']['end']) == float:
           end = int(modVal['cells']['end'] * Populations[modKey].local_size)
        else:
            end = modVal['cells']['end']

        cells = Populations[modKey].local_cells
        for key,value in modVal['properties'].iteritems():
            Populations[modKey][ Populations[modKey].id_to_index(list(cells[ start:end ])) ].set(**{key:value})

    return Populations

def perform_injections(params, populations):
    for modKey,modVal in params['Injections'].iteritems():
        if isinstance(modVal['start'], (list)):
            source = modVal['source'](times=modVal['start'], amplitudes=modVal['amplitude'])
        else:
            source = modVal['source'](amplitude=modVal['amplitude'], start=modVal['start'], stop=modVal['stop'])
        populations[modKey].inject( source )



def record_data(Params, Populations):
    for recPop, recVal in Params['Recorders'].iteritems():
        for elKey,elVal in recVal.iteritems():
            if elVal == 'all':
                Populations[recPop].record( elKey )
            else:
                Populations[recPop][elVal['start']:elVal['end']].record( elKey )


def run_simulation(Params):
    print "Running Network"
    timer = Timer()
    timer.reset()
    run(Params['run_time'])
    simCPUtime = timer.elapsedTime()
    print "Simulation Time: %s" % str(simCPUtime)


def save_data(Populations,folder,addon=''):
    print "saving data"
    for key,p in Populations.iteritems():
        if key != 'ext':
            data = p.get_data()
            p.write_data(folder+'/'+key+addon+'.pkl', annotations={'script_name': __file__})



def analyse(params, folder='results', addon='', removeDataFile=False):
    print "analysing data"
    # populations key-recorders match
    populations = {}
    for popKey,popVal in params['Populations'].iteritems():
        if popKey != 'ext':
            populations[popKey] = params['Recorders'][popKey].keys()
            print popKey, populations[popKey]

    score = {}

    # default results name folder
    if folder=='results':
        dt = datetime.now()
        date = dt.strftime("%d-%m-%I-%M")
        folder = folder+'/'+date

    # iteration over populations and selctive plotting based on available recorders
    for key,rec in populations.iteritems():
        print key

        neo = pickle.load( open(folder+'/'+key+addon+'.pkl', "rb") )
        data = neo.segments[0]

        panels = []
        if 'v' in rec:
            vm = data.filter(name = 'v')[0]
            panels.append( Panel(vm, ylabel="Membrane potential (mV)", xlabel="Time (ms)", xticks=True, yticks=True, legend=None) )
            # Vm histogram
            fig = plot.figure()
            ylabel = key
            n,bins,patches = plot.hist(np.mean(vm,1),50)
            fig.savefig(folder+'/Vm_histogram_'+key+addon+'.png')

        if 'gsyn_exc' in rec and 'gsyn_inh' in rec:
            gsyn_exc = data.filter(name="gsyn_exc")
            gsyn_inh = data.filter(name="gsyn_inh")
            panels.append( Panel(gsyn,ylabel = "Synaptic conductance (uS)",xlabel="Time (ms)", xticks=True,legend = None) )

        if 'spikes' in rec:
            #Panel(rd.sample(data.spiketrains,100), xlabel="Time (ms)", xticks=True, markersize = 1)
            panels.append( Panel(data.spiketrains, xlabel="Time (ms)", xticks=True, markersize=1) )
            # firing rate
            fr = rate(params, data.spiketrains, bin_size=10)
            fig = plot.figure()
            plot.plot(fr)
            fig.savefig(folder+'/firingrate_'+key+addon+'.png')
            fig.clear()

        Figure( *panels ).save(folder+'/'+key+addon+".png")

        # LFP
        if 'v' in rec and 'gsyn_exc' in rec:
            lfp = compute_LFP(data)
            lfp = lfp.reshape((params['run_time']/params['dt']+1.,1))
            v_auxG = 2*lfp[1]-lfp[::-1];
            v_auxR = 2*lfp[-1]-lfp[::-1];
            b,a = signal.iirfilter(2,[0.1*2*params['dt']**2/1000,10*2*params['dt']**2/1000])
            filt_lfp = signal.filtfilt(b, a, np.concatenate((v_auxG,lfp,v_auxR)),axis=0)
            print "lfp",lfp.shape,"filt_lfp",filt_lfp.shape
            vm = data.filter(name = 'v')[0]

            N = lfp.shape[0]
            T = params['dt']
            fft_lfp = np.fft.fft(lfp)
            freq = np.fft.fftfreq(lfp.shape[0],params['dt'])
            #xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
            fig = plot.figure(2)
            plot.subplot(2,1,1)
            plot.plot(lfp)
            plot.subplot(2,1,2)
            #plot.plot(filt_lfp[len(filt_lfp)//3:2*len(filt_lfp)//3])
            #plot.plot(xf, 2.0/N * np.abs(fft_lfp[0:N//2]))
            plot.plot(freq,fft_lfp)
            fig.savefig(folder+'/LFP_'+key+addon+'.png')
            fig.clear()

        ## metric supposed to characterize bimodality
        #bins = bins[:-1]
        #prop_left = sum([n[i] for i,data in enumerate(bins) if bins[i]<(np.mean(vm)-np.std(vm)/2)])/sum(n)
        #prop_right = sum([n[i] for i,data in enumerate(bins) if bins[i]>(np.mean(vm)+np.std(vm)/2)])/sum(n)
        #score[key] = float("{0:.2f}".format(prop_left*prop_right))
        #print "prop_left",prop_left, "prop_right",prop_right
        #print "score",prop_left*prop_right

        # for systems with low memory :)
        if removeDataFile:
            os.remove(folder+'/'+key+addon+'.pkl')

    return score



def compute_LFP(data):
      v = data.filter(name="v")[0]
      g = data.filter(name="gsyn_exc")[0]
      # We produce the current for each cell for this time interval, with the Ohm law:
      # I = g(V-E), where E is the equilibrium for exc, which usually is 0.0 (we can change it)
      # (and we also have to consider inhibitory condictances)
      i = g*(v) #AMPA
      # the LFP is the result of cells' currents
      avg_i_by_t = numpy.sum(i,axis=1)/i.shape[0] #
      sigma = 0.1 # [0.1, 0.01] # Dobiszewski_et_al2012.pdf
      lfp = (1/(4*numpy.pi*sigma)) *  avg_i_by_t
      return lfp



def plot_spiketrains(segment):
    for spiketrain in segment.spiketrains:
        y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
        plot.plot(spiketrain, y,linestyle='dashed', marker='o',markersize =1)
        plot.ylabel(segment.name)
        plot.setp(plot.gca().get_xticklabels(), visible=False)


def plot_signal(signal, index, colour='b'):
    label = "Neuron %d" % signal.annotations['source_ids'][index]
    plt.plot(signal.times, signal[:, index], colour, label=label)
    plt.ylabel("%s (%s)" % (signal.name, signal.units._dimensionality.string))
    plt.setp(plt.gca().get_xticklabels(), visible=False)
    plt.legend()


def load_spikelist( filename, t_start=.0, t_stop=1. ):
    spiketrains = []
    # Data is in Neo format inside a pickle file
    # open the pickle and get the neo block
    neo_block = pickle.load( open(filename, "rb") )
    # get spiketrains
    neo_spikes = neo_block.segments[0].spiketrains
    for i,st in enumerate(neo_spikes):
        for t in st.magnitude:
            spiketrains.append( (i, t) )

    spklist = SpikeList(spiketrains, range(len(neo_spikes)), t_start=t_start, t_stop=t_stop)
    return spklist




def rate( params, spiketrains, bin_size=10 ):
    """
    Binned-time Firing firing rate
    """
    if spiketrains == [] :
        return NaN
    # create bin edges based on number of times and bin size
    bin_edges = np.arange( 0, params['run_time'], bin_size )
    #print "bin_edges",bin_edges.shape
    # binning absolute time, and counting the number of spike times in each bin
    hist = np.zeros( bin_edges.shape[0]-1 )
    for spike_times in spiketrains:
        hist = hist + np.histogram( spike_times, bin_edges )[0]
    return hist / len(spiketrains)
