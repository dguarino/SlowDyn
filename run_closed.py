import NeuroTools.signals
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer
import sys, getopt

import helpers as h


# ----------------

class SetInput(object):
    """
    """

    def __init__(self, populations, interval=20.0, dt=0.1):
        self.interval = interval
        self.populations = populations
        self.dt = dt

    def rythm(self, t, eeg):
        # use the eeg interval (N ms) to compute the input
        spike_times = [t+1, t+3, t+4] # result of the rythm_func
        return spike_times

    def __call__(self, t):
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
                #print 'i',i.shape
                #print i
                # http://www.scholarpedia.org/article/Local_field_potential
                # the LFP is the result of all cells' currents
                avg_i_by_t = numpy.sum(i,axis=0)/i.shape[0] # / time steps
                #print avg_i_by_t.shape
                #print avg_i_by_t
                sigma = 0.1 # [0.1, 0.01] # Dobiszewski_et_al2012.pdf
                lfp = (1/(4*numpy.pi*sigma)) * numpy.sum( avg_i_by_t )
                # a very large LFP would give us a signal comparable to eeg
                # - https://www.quora.com/Neuroscience-What-is-difference-between-local-field-potential-and-EEG
                # - Musall et al 2012
                # - Bartosz (personal communication)
                print lfp
            # LFP into rythm_func
            spike_times = self.rythm(t,lfp)
            self.populations['audio'].set(spike_times=spike_times)
        except StopIteration:
            pass
        return t + self.interval

# ----------------
# one external input source is a spike array
# stimulus = sim.Population(1, sim.SpikeSourceArray(spike_times=spike_times), label="Input spikes")





usage_str = 'usage: run.py -p <param file>'
try:
      opts, args = getopt.getopt(sys.argv[1:], "hp:" )
except getopt.GetoptError:
    print usage_str,"error"
    sys.exit(2)
if len(opts)==0:
    print usage_str,"empty opts"
for opt, arg in opts:
    if opt == '-h':
        print usage_str
        sys.exit()
    elif opt == '-p':
        print arg
        external = __import__(arg)


Populations = h.build_network( external.params )

h.record_data(external.params, Populations)

#h.run_simulation(external.params)
print "Running Network"
timer = Timer()
timer.reset()
interval = 10
run(external.params['run_time'], callbacks=[ SetInput(Populations, interval, external.params['dt']) ])
simCPUtime = timer.elapsedTime()
print "Simulation Time: %s" % str(simCPUtime)

h.save_data(Populations)

end()
