import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
from params import params

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
            y = np.array(p1)
            z = np.array([map(float,data[i]) for i in range(ind*len(p1),(ind+1)*len(p1))])
            z = z[:,0:len(x)]
        else:
            y = np.array(p2)
            indices = np.arange(ind,len(data),len(p1))
            z = np.array([map(float,data[i]) for i in indices ])
            z = z[:,0:len(x)]

        xx,yy=np.meshgrid(x,y)
        grid=np.c_[xx.ravel(),yy.ravel()]

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



def mean_psdmaps(nb_runs,filename):
    for run in range(nb_runs):
        reader = csv.reader( open('results/' + filename+'-'+str(run)+'.csv', 'rb') )
        org_data = list(reader)
        local_data = np.array([map(float,org_data[i]) for i in range(3,len(org_data))])
        if run == 0:
            data = local_data
            print run
        else:
            data = data + local_data
            print run
            
    data[3:,:] /= nb_runs
    with open('results/csvmaps/mapscombinations/down/mean_psd'+'.csv', 'wb') as csvfile:
        mywriter = csv.writer(csvfile)
        mywriter.writerow(org_data[0])
        mywriter.writerow(org_data[1])
        for row in range(data.shape[0]):
            mywriter.writerow(data[row,:])

    x = [freqs[i] for i in range(len(freqs)) if freqs[i]<10]
    mean_psd = np.mean(data[:,:len(x)],0)
    fig = plot.figure()
    for index in range(data.shape[0]):
        plot.plot(x, data[index,:len(x)],'b')
    plot.plot(x,mean_psd[:len(x)],'m')
    plot.xlabel('Frequency')
    #plot.ylim(ymax=2e-8)
    plot.savefig('mean_psd.png')


    return mean_psd        


reader = csv.reader( open('results/csvmaps/mapscombinations/down/psdmap-1.csv', 'rb') )
data = list(reader)
freqs = map(float,data[2])
mean_psd = mean_psdmaps(8,'csvmaps/mapscombinations/down/psdmap')
reader = csv.reader( open('results/csvmaps/mapscombinations/down/mean_psd.csv', 'rb') )
psd_map(reader,axis=1)
reader = csv.reader( open('results/csvmaps/mapscombinations/down/mean_psd.csv', 'rb') )
psd_map(reader,axis=0)



