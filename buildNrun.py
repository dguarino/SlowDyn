import NeuroTools.signals
import numpy.random
import os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer


usage_str = 'usage: run.py -p <param file>'

try:
      opts, args = getopt.getopt( argv, "hp:" )
except getopt.GetoptError:
    print usage_str
    sys.exit(2)
if len(opts)==0:
    print usage_str
for opt, arg in opts:
    if opt == '-h':
        print usage_str
        sys.exit()
    elif opt == '-p':
        params = __import__(arg)


Populations = {}
for pop in params['Populations']:
    Populations[pop.key]= Population( pop['number'], pop['type'], cellparams=pop['params'] )


Projections = {}
for p in params['Projections']:
    Projections[p.key] = Projection(
        Populations[ p['source'] ],
        Populations[ p['target'] ],
        connector = p['connector'],
        synapse_type = p['synapse_type'],
        receptor_type = p['receptor_type']
    )
    print "Number of Synapses ("+p['source']+'_'+p['target'+']):', len(py_inh)


for key in Populations.keys()
    Populations[key].initialize()

for m in  Modifiers:
    cells = m.key.local_cells
#if start ||end = int, absolute number, if end=float, proportion
    if type(m['start']) == float:
        m['start'] = int(m['start']*len(cells))
    if type(m['end']) == float:
        m['end'] = int(m['end']*len(cells))                                            
    cells = cells[ m['start']:m['end'] ]
    for cell in cells:
        cell.a = 0.02e3
        cell.b = 0.0

# Connect Groups - Random Connect
print "Random Connect"
rng = NumpyRNG(1235342134, parallel_safe=False)
    

# Recording
for rec in Recorders:
    for e in rec.key:
        Populations[key].record('spikes')
        Populations[key][0:2].record(('v', 'gsyn_exc','gsyn_inh'))

print "Running Network"
timer = Timer()
timer.reset()
run(run_time)
simCPUtime = timer.elapsedTime()

print "Simulation Time: %s" % str(simCPUtime)
