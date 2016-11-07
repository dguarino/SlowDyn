# encoding: utf-8
"""
Closed loop test based on:
http://neuralensemble.org/docs/PyNN/examples/small_network.html

Small network created with the Population and Projection classes

Usage: small_network_closed_loop.py [-h] [--plot-figure] [--debug DEBUG] simulator
Ex: $ python small_network_closed_loop.py --plot-figure nest

positional arguments:
  simulator      neuron, nest, brian or another backend simulator

optional arguments:
  -h, --help     show this help message and exit
  --plot-figure  plot the simulation results to a file
  --debug DEBUG  print debugging information

"""

import numpy
from pyNN.utility import get_simulator, init_logging, normalized_filename
from pyNN.parameters import Sequence
from pyNN.random import RandomDistribution as rnd
from pyNN.utility import Timer

sim, options = get_simulator(("--plot-figure", "Plot the simulation results to a file.", {"action": "store_true"}),
                             ("--debug", "Print debugging information"))

if options.debug:
    init_logging(None, debug=True)



# === Define Callback Object ===================================================

class SetInput(object):

    def __init__(self, pop_output, pop_input, interval=20.0, dt=0.1):
        self.interval = interval
        self.pop_output = pop_output
        self.pop_input = pop_input
        self.dt = dt


    def generate_spikes(self, lfp):
        # fake function based on lfp driving the spike input generation
        gen = lambda: Sequence(numpy.add.accumulate(numpy.random.exponential(1000.0/50., size=int(abs(lfp) * 20.0))))
        return gen()

    def __call__(self, t):
        try:
            lfp = 0.0
            if t>0.0: # there needs to be data, so after time 0 :)
                data = self.pop_output.get_data().segments[0]
                # get only the last interval recordings
                # during an interval (10ms)
                v = data.filter(name="v")[0][int(t-self.interval)*self.interval:int(t)*self.interval]
                g = data.filter(name="gsyn_exc")[0][int(t-self.interval)*self.interval:int(t)*self.interval]
                # We produce the current for each cell for this time interval, with the Ohm law:
                # I = g(V-E), where E is the equilibrium for exc, which usually is 0.0 (we can change it)
                # (and we also have to consider inhibitory condictances)
                i = g*(v) #AMPA
                # the LFP is the result of cells' currents
                avg_i_by_t = numpy.sum(i,axis=0)/i.shape[0] #
                sigma = 0.1 # [0.1, 0.01] # Dobiszewski_et_al2012.pdf
                lfp = (1/(4*numpy.pi*sigma)) * numpy.sum( avg_i_by_t )
                print lfp
            # LFP into rythm_func
            if abs(lfp) > 0.:
                spike_times = self.generate_spikes(lfp)
                self.pop_input.set(spike_times=spike_times)
        except StopIteration:
            pass
        return t + self.interval


# === Define parameters ========================================================

n = 20      # Number of cells
w = 0.002  # synaptic weight (µS)
cell_params = {
    'tau_m'      : 20.0,   # (ms)
    'tau_syn_E'  : 2.0,    # (ms)
    'tau_syn_I'  : 4.0,    # (ms)
    'e_rev_E'    : 0.0,    # (mV)
    'e_rev_I'    : -70.0,  # (mV)
    'tau_refrac' : 2.0,    # (ms)
    'v_rest'     : -60.0,  # (mV)
    'v_reset'    : -70.0,  # (mV)
    'v_thresh'   : -50.0,  # (mV)
    'cm'         : 0.5     # (nF)
}
dt         = 0.1           # (ms)
syn_delay  = 1.0           # (ms)
input_rate = 50.0          # (Hz)
simtime    = 1000.0        # (ms)


# === Build the network ========================================================

sim.setup(timestep=dt, max_delay=syn_delay)

cells = sim.Population(n, sim.IF_cond_alpha(**cell_params),
                       initial_values={'v': rnd('uniform', (-60.0, -50.0))},
                       label="cells")

number = int(2 * simtime * input_rate / 1000.0)
numpy.random.seed(26278342)
def generate_spike_times(i):
    gen = lambda: Sequence(numpy.add.accumulate(numpy.random.exponential(1000.0 / input_rate, size=number)))
    if hasattr(i, "__len__"):
        return [gen() for j in i]
    else:
        return gen()
assert generate_spike_times(0).max() > simtime

spike_source = sim.Population(n, sim.SpikeSourceArray(spike_times=generate_spike_times))

spike_source.record('spikes')
cells.record(('spikes', 'v', 'gsyn_exc'))

syn = sim.StaticSynapse(weight=w, delay=syn_delay)
input_conns = sim.Projection(spike_source, cells, sim.FixedProbabilityConnector(0.5), syn)

# === Run simulation ===========================================================

print "Running Network"
timer = Timer()
timer.reset()
interval = 10
sim.run(simtime, callbacks=[ SetInput(cells, spike_source, interval, dt) ])
simCPUtime = timer.elapsedTime()
print "Simulation Time: %s" % str(simCPUtime)


filename = normalized_filename("Results", "small_network", "pkl",
                               options.simulator, sim.num_processes())
cells.write_data(filename, annotations={'script_name': __file__})

print("Mean firing rate: ", cells.mean_spike_count() * 1000.0 / simtime, "Hz")

if options.plot_figure:
    from pyNN.utility.plotting import Figure, Panel
    figure_filename = filename.replace("pkl", "png")
    data = cells.get_data().segments[0]
    vm = data.filter(name="v")[0]
    gsyn = data.filter(name="gsyn_exc")[0]
    Figure(
        Panel(vm, ylabel="Membrane potential (mV)"),
        Panel(gsyn, ylabel="Synaptic conductance (uS)"),
        Panel(data.spiketrains, xlabel="Time (ms)", xticks=True),
        annotations="Simulated with %s" % options.simulator.upper()
    ).save(figure_filename)
    print(figure_filename)

# === Clean up and quit ========================================================

sim.end()
