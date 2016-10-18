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

class SetRate(object):
    """
    A callback which changes the firing rate of a population of poisson
    processes at a fixed interval.
    """

    def __init__(self, population, rate_generator, interval=20.0):
        assert isinstance(population.celltype, SpikeSourcePoisson)
        self.population = population
        self.interval = interval
        self.rate_generator = rate_generator

    def __call__(self, t):
        try:
          self.population.set(rate=next(rate_generator))
          print "ciao"
        except StopIteration:
            pass
        return t + self.interval

# ----------------





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
rate_increment = 20
interval = 10
rate_generator = iter(range(0, 500, rate_increment))
run(external.params['run_time'], callbacks=[ SetRate(Populations['ext'], rate_generator, interval) ])
simCPUtime = timer.elapsedTime()
print "Simulation Time: %s" % str(simCPUtime)

h.save_data(Populations)

end()
