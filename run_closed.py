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

    def __init__(self, populations, rate_generator, interval=20.0):
        self.interval = interval
        self.rate_generator = rate_generator
        self.populations = populations

    def __call__(self, t):
        try:
          #print t,"ciao"
          if t>0.0: # there needs to be data, so after time 0 :)
              data = self.populations['py'].get_data().segments[0]
              #print data
              gsyn = data.filter(name="gsyn_exc")
              print gsyn
          self.populations['ext'].set(rate=next(rate_generator))
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
run(external.params['run_time'], callbacks=[ SetRate(Populations, rate_generator, interval) ])
simCPUtime = timer.elapsedTime()
print "Simulation Time: %s" % str(simCPUtime)

h.save_data(Populations)

end()
