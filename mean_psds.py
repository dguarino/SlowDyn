import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot
from matplotlib import cm
from params import params

def mean_psdmaps(nb_runs,filename):
    for run in range(nb_runs):
        reader = csv.reader( open('results/' + filename+'-'+str(run)+'.csv', 'rb') )
        org_data = list(reader)
        local_data = np.array([map(float,org_data[i]) for i in range(3,len(org_data))])
        print local_data.shape
        if run == 0:
            data = local_data
            print run
        else:
            data = data + local_data
            print run
    
    data /= nb_runs

    x = [freqs[i] for i in range(len(freqs)) if freqs[i]<10]
    mean_psd = np.mean(data[:,:len(x)],0)


    return x,mean_psd        


    
reader = csv.reader( open('results/csvmaps/mapscombinations/up/psdmap-py-1.csv', 'rb') )
data = list(reader)
freqs = map(float,data[2])

conds = ['down','up','both']
pops = ['py','tc','re']
colors = ['r','g','b']


for pop in pops:
    print pop
    fig = plot.figure()
    for cond,color in zip(conds,colors):
        print cond
        path = 'csvmaps/mapscombinations/'+cond+'/psdmap-'+ pop
        x,mean_psd = mean_psdmaps(8,path)
        plot.plot(x,mean_psd[:len(x)],color,label=cond)
    plot.xlabel('Frequency')
    plot.ylim(ymax=2e-8)
    plot.legend()
    plot.savefig('mean_psd'+pop+'.png')
    fig.clear()
