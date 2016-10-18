import NeuroTools.signals
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
            p.write_data(key+addon+'.pkl', annotations={'script_name': __file__})


def plot_spiketrains(segment):
    for spiketrain in segment.spiketrains:
        y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
        plt.plot(spiketrain, y, '.')
        plt.ylabel(segment.name)
        plt.setp(plt.gca().get_xticklabels(), visible=False)


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

    for key,p in Populations.iteritems():
        if key != 'ext':
            neo = pickle.load( open(key+filename+'.pkl', "rb") )
            data = neo.segments[0]

            vm_py = data.filter(name = 'v')[0]
            Figure(
                Panel(vm_py, ylabel="Membrane potential (mV)"),
                Panel(data.spiketrains, xlabel="Time (ms)", xticks=True)
            ).save(key+filename+".png")


            fig = plot.figure()
            n,bins,patches = plot.hist(vm_py)
            fig.savefig(key+filename+'hist.png')
            fig.clear()
