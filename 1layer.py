"""
  1 Layer Cortical Network Simulation with a fraction of excitatory cells with LTS

  Destexhe Lab 
  Written in pyNN by Lyle Muller 18 Mar 2010
  Modified by Zahara Gironés 7 June 2016
  
    This file implements a PyNN version of the model detailed in
  Destexhe, A. Self-sustained asynchronous irregular states and
  Up/Down states in thalamic, cortical and thalamocortical
  networks of nonlinear integrate-and-fire neurons.
  Journal of Computational Neuroscience 27: 493-506, 2009. 

  arXiv preprint: http://arxiv.org/abs/0809.0654

 
"""

import NeuroTools.signals,numpy.random,os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer

setup()

### Switch Statements
DistanceDep = True
run_time = 5000.0               # ms
b = .01                         # b = .05 SA, .005 WA
#

# Population Numbers
py_n = 400 #800  #1600                   
inh_n = 100 # 200  #400                   
#

# Synaptic Conductances / External Stimulation
g_e = 6e-3         # nS
g_i = 67e-3        # nS       
g_ext = 6e-3
stim_dur = 50.0
p_c = .02
#scale_factor = round((py_n+inh_n) / (pyB_n+inhB_n)) 
inter_p_c = .01
v_init = -60.0
#

# Parameters

py_params = {'tau_m'      : 20.0,             # ms
               'tau_syn_E'  : 5.0,
               'tau_syn_I'  : 10.0,
               'tau_refrac' : 2.5,
               'v_rest'     : -60.0,
               'v_reset'    : -60.0,
               'v_thresh'   : -50.0,
               'delta_T'    : 2.5,
               'tau_w'      : 600.0,
               'cm'         : 0.200,
               'a'          : 0.001e3,
               'b'          : b   }         
inh_params = {'tau_m'      : 20.0,             # ms
               'tau_syn_E'  : 5.0,
               'tau_syn_I'  : 10.0,
               'tau_refrac' : 2.5,
               'v_rest'     : -60.0,
               'v_reset'    : -60.0,
               'v_thresh'   : -50.0,
               'delta_T'    : 2.5,
               'tau_w'      : 600.0,
               'cm'         : 0.200,
               'a'          : 0.001e3,
               'b'          : 0.0    }

#

print "Building Network"

# Create Populations
py = Population(py_n,EIF_cond_alpha_isfa_ista,cellparams=py_params)
inh = Population(inh_n,EIF_cond_alpha_isfa_ista,cellparams=inh_params)
#

# External Stimulation - Start of Simulation
ext_py = Population(1,SpikeSourcePoisson,cellparams={'start':0.0,'rate':50.,'duration':stim_dur})
ext_prj_py = Projection(ext_py,py,FixedProbabilityConnector(.02,weights=g_ext,delays=None),target='excitatory')


#
py.initialize("v", v_init)
inh.initialize("v", v_init)
                  

# LTS Subgroup - 10% of Layer #B
cells = py.local_cells
#cells = numpy.random.permutation(cells)[0:int(0.1*len(cells))]
cells = cells[0:int(0.1*len(cells))]

for cell in cells:
    cell.a = 0.02e3
    cell.b = 0.0

# Connect Groups - Random Connect 
print "Random Connect" 
rng = NumpyRNG(1235342134, parallel_safe=False)

py_py = Projection(py,py,method=FixedProbabilityConnector(p_c,allow_self_connections=False,weights=g_e,delays=None),target='excitatory',rng=rng)   
print "Number of Synapses (py_py):", len(py_py)

py_inh = Projection(py,inh,FixedProbabilityConnector(p_c,allow_self_connections=False,weights=g_e,delays=None),target='excitatory',rng=rng)   
print "Number of Synapses (py_inh):", len(py_inh)

inh_py = Projection(inh,py,FixedProbabilityConnector(p_c,allow_self_connections=False,weights=g_i,delays=None),target='inhibitory',rng=rng)
print "Number of Synapses (inh_py):", len(inh_py)   

inh_inh = Projection(inh,inh,FixedProbabilityConnector(p_c,allow_self_connections=False,weights=g_i,delays=None),target='inhibitory',rng=rng)   
print "Number of Synapses (inh_inh):", len(inh_inh)

# Recording
##py.record_v(10)
##inh.record_v(10)
py.record()
inh.record()
#

print "Running Network"
timer = Timer()
timer.reset()
run(run_time)
simCPUtime = timer.elapsedTime()

print "Simulation Time: %s" % str(simCPUtime)

##os.chdir('Insert Data Directory Here')
##py.print_v('pyB_v.dat')
##inh.print_v('inhB_v.dat')
py.printSpikes('py_1layer.dat')
inh.printSpikes('inh_1layer.dat')

##py_py.saveConnections('py_py005.conn')


'''  This is done in a separate scipt called 1layer_analysis.py '''
'''
plot.ion()

py_sp = NeuroTools.signals.load_spikelist('py_1layer.dat')
print "Layer A Pyramidal Mean Rate (initial stimulation): %s" % str(py_sp.mean_rate(t_start=0,t_stop=stim_dur))
print "Layer A Pyramidal Mean Rate: %s" % str(py_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
print "Layer A Pyramidal Mean CV: %s" % str(mean(py_sp.cv_isi(float_only=True)))
py_sp.raster_plot(display=plot.subplot(221))
plot.ylabel('PY Layer A')
plot.xlabel('')
plot.title('b = %s' % str(b))

inh_sp = NeuroTools.signals.load_spikelist('inh_1layer.dat')
#print inh_sp
#print inh_sp.mean_rate(t_start=28, t_stop=stim_dur)
#print stim_dur
print "Layer A Interneuron Mean Rate (initial stimulation): %s" % str(inh_sp.mean_rate(t_start=0,t_stop=stim_dur))
print "Layer A Interneuron Mean Rate: %s" % str(inh_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
print "Layer A Interneuron Mean CV: %s" % str(mean(inh_sp.cv_isi(float_only=True)))
inh_sp.raster_plot(display=plot.subplot(222))
plot.ylabel('INH Layer A')
plot.xlabel('')


plot.savefig('raster_1layer.pdf')
'''

# Cleanup
end()
#
