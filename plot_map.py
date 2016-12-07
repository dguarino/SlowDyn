import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot
from params import params

def plot_map( csvfile, factor=100 ):
    data = list(csvfile)
    header1 = data.pop(0)[0]
    text1, p1 = header1.strip('#').split(':')
    p1 = eval(p1)
    header2 = data.pop(0)[0]
    text2, p2 = header2.strip('#').split(':')
    p2 = eval(p2)
    #axis1 = [ i for j in p2 for i in p1 ]
    axis1 = [ i for j in p2 for i in p1[:-1] ]
    #axis2 = [ j for j in p2 for i in p1 ]
    axis2 = [ j for j in p2 for i in p1[:-1] ]
    combinations = len(p1) * len(p2)
    area = np.zeros(combinations)
    colors = np.zeros(combinations)
    marks = ['o' for i in range(combinations)]

    i = 0
    for row in data:
        for col in row[:-1]:
        #for col in row:
            pair = eval(col)
            colors[i] = float(pair[1]) # color for freq
            size = float(pair[0]) # size for ratio
            # size for ratio
            # we want to be able to see whether the ratio is towards short-up, equal, or long-up
            if 0 < size < 0.5:
                size = 1. - size
                marks[i] = 's' # but we change their marker to diversify
            area[i] = size * factor
          
            i=i+1

    # normalize colors for matplotlib
    fig = plot.figure(1)
    norm = ml.colors.Normalize(vmin=min(colors), vmax=max(colors), clip=True)
    mapper = ml.cm.ScalarMappable(norm=norm, cmap=plot.cm.jet)
    mapper._A = [] # hack to plot the colorbar http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    mapper.set_clim(0.,4.)
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1, rotation='vertical')
    plot.yticks(p2)
    #plot.xlim([.0000001,.1]) # TODO: remove!!!! hack just to plot the TC param search
    for x,y,a,c,m in zip(axis1,axis2,area,colors,marks):
        #print x,y,a,c
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none')
    cbar = plot.colorbar(mapper)
    cbar.ax.set_ylabel('largest frequency', rotation=270)
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.tick_params(axis='both', which='minor', labelsize=8)
    #plot.xscale('log') # TODO: remove!!!! hack just to plot the TC param search
    plot.savefig('search_map.png')
    fig.clear()


def plot_var_map( csvfile, std, factor = 100):
    data = list(csvfile)
    print "file read"
    header1 = data.pop(0)[0]
    text1, p1 = header1.strip('#').split(':')
    p1 = eval(p1)
    header2 = data.pop(0)[0]
    text2, p2 = header2.strip('#').split(':')
    p2 = eval(p2)
    axis1 = [ i for j in p2 for i in p1[:-1] ]
    axis2 = [ j for j in p2 for i in p1[:-1] ]
    combinations = len(p1) * len(p2)
    area = np.zeros(combinations)
    colors = np.zeros(combinations)
    marks = ['o' for i in range(combinations)]
    i = 0
    for row in data:
        for col in row[:-1]:
            pair = eval(col)
            colors[i] = float(pair[1]) # color for f
            size = std[i//std.shape[0],i%std.shape[0]] # size for std
            # size for ratio
            # we want to be able to see whether the ratio is towards short-up, equal, or long-up
            area[i] = size * factor
            i=i+1

    # normalize colors for matplotlib
    fig = plot.figure(1)
    norm = ml.colors.Normalize(vmin=min(colors), vmax=max(colors), clip=True)
    mapper = ml.cm.ScalarMappable(norm=norm, cmap=plot.cm.jet)
    mapper._A = [] # hack to plot the colorbar http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    mapper.set_clim(vmin = 0.,vmax = 4.)
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1, rotation='vertical')
    plot.yticks(p2)
    plot.yticks([3.])
    #plot.xlim([.0000001,.1]) # TODO: remove!!!! hack just to plot the TC param search
    for x,y,a,c,m in zip(axis1,axis2,area,colors,marks):
        #print x,y,a,c
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none')
    cbar = plot.colorbar(mapper)
    cbar.ax.set_ylabel('largest frequency', rotation=270)
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.tick_params(axis='both', which='minor', labelsize=8)
    #plot.xscale('log') # TODO: remove!!!! hack just to plot the TC param search
    plot.savefig('var_map.png')
    fig.clear()


def mean_maps(nb_runs,filename):
    for run in range(nb_runs):
        print run
        reader = csv.reader( open('results/' + filename+'-'+str(run)+'.csv', 'rb') )
        data = list(reader)
        if run == 0:
            mean_data = data
        local_data = np.array([data[i] for i in range(2,len(data))])
        fqcy = np.zeros((local_data.shape[0],local_data.shape[1],params['nb_runs']))
        for i in range(len(local_data)):
            for j in range(len(local_data[i])):
                if run == 0:
                    mean_data[i+2][j] = np.array(eval(local_data[i][j]))
                else:
                    mean_data[i+2][j] = mean_data[i+2][j] + np.array(eval(local_data[i][j]))
                fqcy[i,j,run] = np.array(eval(local_data[i][j]))[1]
        print np.array(eval(local_data[5][8]))
    
    for i in range(len(local_data)):
         for j in range(len(local_data[i])):
             mean_data[i+2][j] = (mean_data[i+2][j]/nb_runs).tolist()
    print mean_data[5][8]
    std = np.std(fqcy,2)
     
    with open('results/csvmaps/mapsLTS/mean_map'+'.csv', 'wb') as csvfile:
        mywriter = csv.writer(csvfile)
        for row in range(len(mean_data)):
            mywriter.writerow(mean_data[row])

    return std



# using the function...
factor = 100
#plot_map(reader, factor)
std = mean_maps(8,'csvmaps/mapsLTS/map.2')
reader = csv.reader( open('results/csvmaps/mapsLTS/mean_map.csv', 'rb') )
plot_var_map(reader,std,factor)
reader = csv.reader( open('results/csvmaps/mapsLTS/mean_map.csv', 'rb') )
plot_map(reader)
