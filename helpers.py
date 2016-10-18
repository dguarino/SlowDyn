import NeuroTools.signals
import numpy.random
import os
from numpy import *
from pyNN.nest import *
from pyNN.utility import Timer


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


def save_data(Populations):
    for key,p in Populations.iteritems():
        if key != 'ext':
            data = p.get_data()
            p.write_data(key+'.pkl', annotations={'script_name': __file__})


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


def analyse_data():

    # Pyramidal
    py_sp = load_spikelist('py.pkl', t_start=.0, t_stop=run_time)
    print "Layer A Pyramidal Mean Rate (initial stimulation): %s" % str(py_sp.mean_rate(t_start=0,t_stop=stim_dur))
    print "Layer A Pyramidal Mean Rate: %s" % str(py_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
    print "Layer A Pyramidal Mean CV: %s" % str(mean(py_sp.cv_isi(float_only=True)))
    py_sp.raster_plot(display=plot.subplot(221))
    plot.ylabel('PY Layer A')
    plot.xlabel('Time (ms)')
    plot.title('b = %s' % str(b))
    plot.axhline(y=.1*N,linewidth=2,color='r')


    # Inhibitory
    inh_sp = load_spikelist('inh.pkl', t_start=.0, t_stop=run_time)
    print "Layer A Interneuron Mean Rate (initial stimulation): %s" % str(inh_sp.mean_rate(t_start=0,t_stop=stim_dur))
    print "Layer A Interneuron Mean Rate: %s" % str(inh_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
    print "Layer A Interneuron Mean CV: %s" % str(mean(inh_sp.cv_isi(float_only=True)))
    inh_sp.raster_plot(display=plot.subplot(222))
    plot.ylabel('INH Layer A')
    plot.xlabel('Time (ms)')
    plot.title('N = %s' % str(N))

    plot.savefig('raster.png')
