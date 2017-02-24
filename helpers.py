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

from __future__ import division
import NeuroTools.signals
import numpy as np
import random as rd
import os
import scipy.io
import pickle
import matplotlib.pyplot as plot
import quantities as pq
from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel
from datetime import datetime
from matplotlib import mlab
from neo.core import AnalogSignalArray


def build_network(sim, Params):
    #creates populations and connections from parameter file
    sim.setup( timestep=Params['dt'])

    Populations = {}
    for popKey,popVal in Params['Populations'].iteritems():
        if isinstance(popVal['n'],dict):
            number = int(Params['Populations'][popVal['n']['ref']]['n'] * popVal['n']['ratio'])
            Populations[popKey] = sim.Population( number, popVal['type'], cellparams=popVal['cellparams'] )
        else:
            Populations[popKey] = sim.Population( popVal['n'], popVal['type'], cellparams=popVal['cellparams'] )

    Projections = {}
    for projKey,projVal in Params['Projections'].iteritems():
        Projections[projKey] = sim.Projection(
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
    #defines what will be recorded
    for recPop, recVal in Params['Recorders'].iteritems():
	print recPop,recVal
        for elKey,elVal in recVal.iteritems():
            if elVal == 'all':
                Populations[recPop].record( elKey )
            else:
                Populations[recPop][elVal['start']:elVal['end']].record( elKey )


def run_simulation(sim,Params):
    print "Running Network"
    timer = Timer()
    timer.reset()
    sim.run(Params['run_time'])
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

    score = {}
    ratio = {}
    fqcy = {}
    psd = {}
    freqs_psd = {}
    fqcy_ratio = {}


    # if the result folder is not specified within results, its name will be the date
    if folder == 'results':
        dt = datetime.now()
        date = dt.strftime("%d-%m-%I-%M")
        folder = folder+'/'+date

    # iteration over populations and selective plotting based on available recorders
    gen = ([key,rec] for key,rec in populations.iteritems() if key != 'ext')
    for key,rec in gen:
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
            fig.clear()

        if 'gsyn_exc' in rec:
            gsyn_exc = data.filter(name="gsyn_exc")[0]
            panels.append( Panel(gsyn_exc,ylabel = "Exc Synaptic conductance (uS)",xlabel="Time (ms)", xticks=True, legend=None) )

        if 'gsyn_inh' in rec:
            gsyn_inh = data.filter(name="gsyn_inh")[0]
            panels.append( Panel(gsyn_inh,ylabel = "Inh Synaptic conductance (uS)",xlabel="Time (ms)", xticks=True, legend=None) )

        if 'spikes' in rec:
            panels.append( Panel(data.spiketrains, xlabel="Time (ms)", xticks=True, markersize=1) )
            bin_size = 10
            minlen = 5 # 50ms : minimal duration for an upstate as in Renart et al 2010
            fr = rate(params, data.spiketrains, bin_size=bin_size)
            # ratio (and additions to figure)
            fig = plot.figure(56)

	    #computes a ratio that indicates if there is more upstate then downstate or the contrary
            #clr = 'black'
            #threshold = 0.25#np.max(fr)/2
            #crossings = np.where(fr > threshold)[0]
            #ups = []
            # group the up bins by their duration (consecutive indexes together)
            #for group in np.split(crossings, np.where(np.diff(crossings)!=1)[0]+1):
            #    if len(group) > minlen:
            #        ups.append(group)
            #uptimes = np.concatenate(ups)
            #uppoints = np.ones(len(uptimes)) * threshold
            #plot.scatter(uptimes, uppoints) # plot chosen up at the threshold
            #ratio = len(uptimes) / (len(fr)-len(uptimes))
            cut_value = int(max(len(data.spiketrains[0])/(bin_size),50))
            dies = sum(np.abs(fr[-cut_value:-1])) < 1/10*min(np.abs(fr))
            if dies:
                ratio[key] = 0.
            else:
                ratio[key] = 1.
            clr = str(ratio[key])

            plot.plot(fr,color=clr,linewidth=2)
            plot.ylim([.0,1.])
            fig.savefig(folder+'/firingrate_'+key+addon+'.png')
            fig.clear()
        
        if params['Injections']:
            amplitude = np.array([0.]+params['Injections']['LTS']['amplitude']+[0.])#[0.,-.25, 0.0, .25, 0.0, 0.]
            start = np.array([0.]+params['Injections']['LTS']['start']+[params['run_time']])/params['dt']
            current = np.array([])

            for i in range(1,len(amplitude)):
                if current.shape == (0,):
                    current = np.ones((start[i]-start[i-1]+1,1))*amplitude[i-1]
                else:
                    current = np.concatenate((current,np.ones((start[i]-start[i-1],1))*amplitude[i-1]),0)
            current = AnalogSignalArray(current, units = 'mA',sampling_rate = params['dt']*pq.Hz)
            current.channel_index = np.array([0])
            panels.append( Panel(current,ylabel = "Current injection (mA)",xlabel="Time (ms)", xticks=True, legend=None) )

        Figure( *panels ).save(folder+'/'+key+addon+".png")
	
        # LFP
        if 'v' in rec and ('gsyn_exc' in rec or 'gsyn_inh' in rec):
	    #compute LFP, spectrum, and dominant frequency
            lfp = compute_LFP(data)
            fe = 1/params['dt']*1000
            psd[key],freqs_psd[key] = mlab.psd(lfp, Fs = fe, NFFT=int(len(lfp)/4))
            x = [freqs_psd[key][i] for i in range(len(freqs_psd[key])) if freqs_psd[key][i]<10.]
            argm = np.argmax(abs(psd[key]))
            fqcy[key] = freqs_psd[key][argm]
            N = len(lfp)
            t = np.arange(0.,N)/fe
            fqcy_ratio[key] = compute_fqcyratio(psd[key],freqs_psd[key])

            fig = plot.figure(2)

            plot.subplot(2,1,1)
            plot.plot(t,lfp,'b')
	    plot.hold(True)
            if 'audio' in params['Populations'].keys():
		neo = pickle.load( open(folder+'/'+'audio'+addon+'.pkl', "rb") )
        	data_audio = neo.segments[0]
		bin_size = 10
		fr = rate(params, data_audio.spiketrains, bin_size=bin_size)
		fr = fr*(np.max(lfp)/2/max(max(fr),0.1))
		plot.subplot(2,1,1)
		plot.plot(np.linspace(0,params['run_time']/1000,len(fr)),fr,'k')

            plot.subplot(2,1,2)
            plot.plot(x,psd[key][0:len(x)])	    
            fig.savefig(folder+'/LFP_'+key+addon+'.png')
            fig.clear()

        # for systems with low memory :)
        if removeDataFile:
            os.remove(folder+'/'+key+addon+'.pkl')

    return ratio,fqcy, psd, freqs_psd, fqcy_ratio


def compute_fqcyratio(psd,freqs_psd):
      #computes the ratio between the largest frequency and all the others, 
      # to see how dominant it is

      max = np.max(abs(psd))
      argm = np.argmax(abs(psd))
      others = sum(psd[i] for i in range(len(freqs_psd)) if (freqs_psd[i] != freqs_psd[argm] and psd[i]>max/2))
      if others == 0:
          fqcy_ratio = 1
      else:
          fqcy_ratio = max/others
      return fqcy_ratio


def compute_LFP(data):
      v = data.filter(name="v")[0]
      g_exc = data.filter(name="gsyn_exc")[0]
      g_inh = data.filter(name="gsyn_inh")[0]
      # We produce the current for each cell for this time interval, with the Ohm law:
      # I = g(V-E), where E is the equilibrium for exc, which usually is 0.0 (we can change it)
      # (and we also have to consider inhibitory condictances)
      i = (g_exc + g_inh) * v #AMPA
      # the LFP is the result of cells' currents
      avg_i_by_t = np.sum(i,axis=1)/i.shape[0] #
      sigma = 0.1 # [0.1, 0.01] # Dobiszewski_et_al2012.pdf
      lfp = (1/(4*np.pi*sigma)) * avg_i_by_t
      lfp = lfp - np.mean(lfp)
      return lfp

	


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
