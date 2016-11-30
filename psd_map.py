import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm

def psd_map( csvfile, axis=1):
    #axis = 0 means that we represent variation of psd with a for different values of b,
    #axis = 1 means it is the other way around
    data = list(csvfile)
    header1 = data.pop(0)[0]
    text1, p1 = header1.strip('#').split(':')
    p1 = eval(p1)
    header2 = data.pop(0)[0]
    text2, p2 = header2.strip('#').split(':')
    p2 = eval(p2)
    freqs = map(float,data[0])
    data = data[1:]
    zmax = np.max([map(float,data[i]) for i in range(len(data))])
    
    if axis == 0:
        nb_maps = len(p2)
    else:
        nb_maps = len(p1)

    for ind in range(nb_maps):
        x = np.array([freqs[i] for i in range(len(freqs)) if freqs[i]<5.])
        if axis == 0:
            y = np.array(p1[:-1])
            z = np.array([map(float,data[i]) for i in range(ind*len(p1),(ind+1)*len(p1)-1)])
            z = z[:,0:len(x)]
        else:
            y = np.array(p2)
            indices = np.arange(ind,len(data),len(p1))
            z = np.array([map(float,data[i]) for i in indices ])
            z = z[:,0:len(x)]

        xx,yy=np.meshgrid(x,y)
        grid=np.c_[xx.ravel(),yy.ravel()]
        print xx.shape, yy.shape, z.shape

        fig = plot.figure(1)
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(xx, yy, z, rstride=1, cstride=1, cmap=cm.gist_rainbow,linewidth=0, antialiased=False, vmax = zmax)
        fig.colorbar(surf)
        ax.set_zlim3d(0,zmax)
        plot.xlabel('Frequency')
        #plot.xticks( map(lambda x: round(x,2),x), rotation = 'vertical')
        if axis == 0:
            plot.ylabel(text1)
            plot.yticks(p1)
            plot.savefig('psd_map'+text2+str(p2[ind])+'.png')
        else:
            plot.ylabel(text2)
            plot.yticks(p2)
            plot.savefig('psd_map'+text1+str(p1[ind])+'.png')
        fig.clear()


  
    
reader = csv.reader( open('results/1layer0.O5LTS0/psdmap.csv', 'rb') )
psd_map(reader,axis=1)
