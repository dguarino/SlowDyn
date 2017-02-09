#reads the search file with the parameter values
#for each pair of values, calls the corresponding psd
#computes the locking score by averaging over the different runs
#plots a graph that represents what has been computed

from __future__ import division


import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib as ml
import pylab as P


pops = ['py']#,'inh'] #populations to take into account
bin = 0.25 #frequency bin in Hz 
map_path = 'smallnet_pushPy+Inh'
nb_runs = 7 #number of runs for this path
nb_harms = 10 #number of harmonics



reader = csv.reader( open('/media/eloise/EC741CFE741CCCE8/results/'+map_path + '0/psdmap-'+pops[0]+'.csv', 'rb') )
data = list(reader)
freqs = [eval(data[2][i]) for i in range(len(data[2]))]	
freqs_red = [freqs[w] for w in range(len(freqs)) if freqs[w] < 15.]
header1 = data.pop(0)[0]
text1, p1 = header1.strip('#').split(':')
header2 = data.pop(0)[0]
text2, p2 = header2.strip('#').split(':')


if text1 == 'push_interval':
    values1 = eval(p1)
    values2 = eval(p2)
    axis1 = [ i for j in eval(p2) for i in eval(p1) ]
    axis2 = [ j for j in eval(p2) for i in eval(p1) ]
    assert(text2 == 'nb_push')
else:
    values1 = eval(p2)
    values2 = eval(p1)
    axis1 = [ i for j in eval(p1) for i in eval(p2) ]
    axis2 = [ j for j in eval(p1) for i in eval(p2) ]
    assert(text2 == 'push_interval' and text1 == 'nb_push')


print "push_intervals : ",values1, "push_strength : ",values2


for pop in pops:
    
    for i,interval in enumerate(values1):
	print i/len(values1)*100,"%"
	push_fqcy = 1000/interval #interval in ms
	harms = [push_fqcy*l for l in range(1,nb_harms+1)]
	print "harms", harms
        bars = {}

        for run in range(nb_runs):
            reader = csv.reader( open('/media/eloise/EC741CFE741CCCE8/results/'+map_path + str(run) + '/psdmap-'+pop+'.csv', 'rb') )
	    data = list(reader)

            for j,push_strength in enumerate(values2):
		psd = data[j*len(values1)+i+3] #load the psd that corresponds to these values
		psd = [eval(psd[n]) for n in range(len(psd))]
		if run == 0:
	       	    bars[push_strength] = []
                for harm in harms:
		    amplitude = sum([psd[u] for u in range(len(psd)) if np.abs(freqs[u]-harm) < bin/2])
    		    bars[push_strength] += (np.ones((1,int(amplitude*1e11/nb_runs)))*harm).tolist()[0]
	print bars.keys()

	colors = ['k','r','g','b','m']
	P.figure()
	n, bins, patches = P.hist( [bars[push_strength] for push_strength in values2], 15, histtype='bar',
            color = colors ,
	    label = values2)
	P.legend()
	P.ylim(0.0,2000.0)
	P.title('Push frequency'+str(push_fqcy)+', '+ str(nb_runs)+'trials')
	P.savefig('push_bar_fqcy='+str(push_fqcy)+pop+'.png')


		
