# Analysis file
import NeuroTools.signals
from NeuroTools.signals import SpikeList, SpikeTrain
import NeuroTools.io
import pickle
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
from pyNN.utility.plotting import Figure, Panel


N= 500 # 1000               # Total number of neurons
run_time = 500.               # ms
b = .01                     # b = .05 SA, .005 WA
stim_dur = 100.0


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


#stat = open("stat.txt", "w+")
#stat.write("Number of neurons= %s" % str(N))
#stat.write("  b = %s" % str(b))
#stat.write("  Layer A Pyramidal Mean Rate (initial stimulation): %s" % str(py_sp.mean_rate(t_start=0,t_stop=stim_dur)));
#stat.write("  Layer A Pyramidal Mean Rate: %s" % str(py_sp.mean_rate(t_start=stim_dur,t_stop=run_time)));
#stat.write("  Layer A Pyramidal Mean CV: %s" % str(mean(py_sp.cv_isi(float_only=True))));
#stat.write("  Layer A Interneuron Mean Rate (initial stimulation): %s" % str(inh_sp.mean_rate(t_start=0,t_stop=stim_dur)));
#stat.write("  Layer A Interneuron Mean Rate: %s" % str(inh_sp.mean_rate(t_start=stim_dur,t_stop=run_time)));
#stat.write("  Layer A Interneuron Mean CV: %s" % str(mean(inh_sp.cv_isi(float_only=True))));
#stat.close()


neo_py = pickle.load( open('py.pkl', "rb") )
neo_inh = pickle.load( open('inh.pkl','rb') )

data_py = neo_py.segments[0]
data_inh = neo_inh.segments[0]

vm_py = data_py.filter(name = 'v')[0]
vm_inh = data_inh.filter(name = 'v')[0]

Figure(
    Panel(vm_py, ylabel="Membrane potential (mV)"),
    Panel(data_py.spiketrains, xlabel="Time (ms)", xticks=True)
).save("py_results.png")


Figure(
    Panel(vm_inh, ylabel="Membrane potential (mV)"),
    Panel(data_inh.spiketrains, xlabel="Time (ms)", xticks=True)
).save("inh_results.png")


fig = plot.figure()
n,bins,patches = plot.hist(vm_py)
fig.savefig('histogramme.png')
