import NeuroTools.signals,numpy.random,os
from pyNN.nest import *
from numpy import *
import matplotlib.pyplot as plot
from pyNN.utility import Timer


N= 500 # 1000                          # Total number of neurons  
run_time = 5000.0               # ms
b = .01                        # b = .05 SA, .005 WA
stim_dur = 50.0


py_sp = NeuroTools.signals.load_spikelist('py_1layer.dat')
print "Layer A Pyramidal Mean Rate (initial stimulation): %s" % str(py_sp.mean_rate(t_start=0,t_stop=stim_dur))
print "Layer A Pyramidal Mean Rate: %s" % str(py_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
print "Layer A Pyramidal Mean CV: %s" % str(mean(py_sp.cv_isi(float_only=True)))
py_sp.raster_plot(display=plot.subplot(221))
plot.ylabel('PY Layer A')
plot.xlabel('Time (ms)')
plot.title('b = %s' % str(b))
#plot.axhline(y=.1*py_n,linewidth=2,color='r')



inh_sp = NeuroTools.signals.load_spikelist('inh_1layer.dat')
print inh_sp.mean_rate(t_start=50, t_stop=run_time)
print stim_dur
print "Layer A Interneuron Mean Rate (initial stimulation): %s" % str(inh_sp.mean_rate(t_start=0,t_stop=stim_dur))
print "Layer A Interneuron Mean Rate: %s" % str(inh_sp.mean_rate(t_start=stim_dur,t_stop=run_time))
#print "Layer A Interneuron Mean CV: %s" % str(mean(inh_sp.cv_isi(float_only=True)))
inh_sp.raster_plot(display=plot.subplot(222))
plot.ylabel('INH Layer A')
plot.xlabel('Time (ms)')
plot.title('N = %s' % str(N))



plot.savefig('raster_1layer.pdf')


stat = open("stat.txt", "w+")
stat.write("Number of neurons= %s" % str(N));

stat.write("  b = %s" % str(b));

stat.write("  Layer A Pyramidal Mean Rate (initial stimulation): %s" % str(py_sp.mean_rate(t_start=0,t_stop=stim_dur)));

stat.write("  Layer A Pyramidal Mean Rate: %s" % str(py_sp.mean_rate(t_start=stim_dur,t_stop=run_time)));

stat.write("  Layer A Pyramidal Mean CV: %s" % str(mean(py_sp.cv_isi(float_only=True))));

stat.write("  Layer A Interneuron Mean Rate (initial stimulation): %s" % str(inh_sp.mean_rate(t_start=0,t_stop=stim_dur)));

stat.write("  Layer A Interneuron Mean Rate: %s" % str(inh_sp.mean_rate(t_start=stim_dur,t_stop=run_time)));

stat.write("  Layer A Interneuron Mean CV: %s" % str(mean(inh_sp.cv_isi(float_only=True))));

stat.close()


# Cleanup
end()
#
