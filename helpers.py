import NeuroTools.signals
import numpy as np
import numpy.random
import os
from numpy import *
from pyNN.nest import *
from pyNN.utility import Timer
import pickle
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plot


def build_network(Params):
    setup( timestep=Params['dt'])

    Populations = {}
    for popKey,popVal in Params['Populations'].iteritems():
        Populations[popKey]=Population( popVal['n'], popVal['type'], cellparams=popVal['cellparams'] )
        #print Populations

    Projections = {}
    for projKey,projVal in Params['Projections'].iteritems():
        Projections[projKey] = Projection(
            Populations[ projVal['source'] ],
            Populations[ projVal['target'] ],
            connector = projVal['connector'],
            synapse_type = projVal['synapse_type'],
            receptor_type = projVal['receptor_type']
        )
       # print "Number of Synapses ("+p['source']+'_'+p['target'+']):', len(py_inh)

    for key in Populations.keys():
        Populations[key].initialize()

    for modKey,modVal in Params['Modifiers'].iteritems():
        cells = Populations[modKey].local_cells
        if type(modVal['cells']['start']) == float:
            start = int(modVal['cells']['start']*len(cells))
        else:
            start = modVal['cells']['start']
        if type(modVal['cells']['end']) == float:
           end = int(modVal['cells']['end']*len(cells))
        else:
            end = modVal['cells']['end']
        cells = cells[ start:end ]
        for cell in cells:
            for key,value in modVal['properties'].iteritems():
                cell.key = value

    return Populations


def record_data(Params, Populations):
    for recPop, recVal in Params['Recorders'].iteritems():
        for elKey,elVal in recVal.iteritems():
            Populations[recPop][elVal['start']:elVal['end']].record( elKey )


def run_simulation(Params):
    print "Running Network"
    timer = Timer()
    timer.reset()
    run(Params['run_time'])
    simCPUtime = timer.elapsedTime()
    print "Simulation Time: %s" % str(simCPUtime)


def save_data(Populations,addon=''):
    for key,p in Populations.iteritems():
        if key != 'ext':
            data = p.get_data()
            p.write_data('results/'+key+addon+'.pkl', annotations={'script_name': __file__})


def plot_spiketrains(segment):
    for spiketrain in segment.spiketrains:
        y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
        plot.plot(spiketrain, y, '.')
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


def analyse(Populations,filename):
    
    pop_number = len(Populations) - 1
    pop_index = 0
    for key,p in Populations.iteritems():
        if key != 'ext':
            pop_index = pop_index + 1
            neo = pickle.load( open('results/'+key+filename+'.pkl', "rb") )
            data = neo.segments[0]

            vm = data.filter(name = 'v')[0]
            gsyn_exc = data.filter(name="gsyn_exc")
            gsyn_inh = data.filter(name="gsyn_inh")
            if not gsyn_exc:
                gsyn = gsyn_inh[0]
            else:
                gsyn = gsyn_exc[0]

           # all on same plot      
           # fig = plot.figure(1)
           # plot.subplot(pop_number*3,1,1+3*(pop_index-1))
           # plot.plot(vm)
           # plot.ylabel("Membrane potential (mV)")
           # plot.subplot(pop_number*3,1,2+3*(pop_index-1))
           # plot.plot(gsyn)
           # plot.ylabel("Synaptic conductance (uS)")
           # plot.subplot(pop_number*3,1,3+3*(pop_index-1))
           # plot_spiketrains(data)
           # plot.xlabel("Time (ms)")
           # plot.setp(plot.gca().get_xticklabels(), visible=True)
           # fig.savefig(filename+".png")

            Figure(
                Panel(vm, ylabel="Membrane potential (mV)",legend = None),
                Panel(gsyn,ylabel = "Synaptic conductance (uS)",legend = None),
                Panel(data.spiketrains, xlabel="Time (ms)", xticks=True)
             ).save('results/'+key+'-'+filename+".png")


            fig = plot.figure(2)
            plot.subplot(pop_number,1,pop_index)
            n,bins,patches = plot.hist(np.mean(vm,0))
            fig.savefig('results/'+filename+'hist.png')
            
            if pop_index == pop_number :
                fig.clear()
