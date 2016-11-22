import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot

def plot_map( csvfile, factor=100 ):
    data = list(csvfile)
    header1 = data.pop(0)[0]
    text1, p1 = header1.strip('#').split(':')
    p1 = eval(p1)
    header2 = data.pop(0)[0]
    text2, p2 = header2.strip('#').split(':')
    p2 = eval(p2)
    axis1 = [ i for j in p2 for i in p1 ]
    axis2 = [ j for j in p2 for i in p1 ]
    combinations = len(p1) * len(p2)
    area = np.zeros(combinations)
    colors = np.zeros(combinations)
    marks = ['o' for i in range(combinations)]

    i = 0
    for row in data:
        for col in row:
            pair = eval(col)
            colors[i] = float(pair[1]) # color for freq
            size = float(pair[0]) # size for ratio
            # size for ratio
            # we want to be able to see whether the ratio is towards short-up, equal, or long-up
<<<<<<< HEAD
            if 0 < size < 0.5:
                size = 1. - size
=======
            if size < 1.:
>>>>>>> 40c51a6c43c0a6fdc302a27fc61278d818416540
                marks[i] = 's' # but we change their marker to diversify
            area[i] = size * factor
            i=i+1

    # normalize colors for matplotlib
    fig = plot.figure(1)
    norm = ml.colors.Normalize(vmin=min(colors), vmax=max(colors), clip=True)
    mapper = plot.cm.ScalarMappable(norm=norm, cmap=plot.cm.jet)
    mapper._A = [] # hack to plot the colorbar http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1, rotation='vertical')
    plot.yticks(p2)
    for x,y,a,c,m in zip(axis1,axis2,area,colors,marks):
        #print x,y,a,c
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none')
    cbar = plot.colorbar(mapper)
    cbar.ax.set_ylabel('largest frequency', rotation=270)
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.tick_params(axis='both', which='minor', labelsize=8)

    plot.savefig('search_map.png')
    fig.clear()

# using the function...
factor = 100
reader = csv.reader( open('results/1layer/map.csv', 'rb') )
plot_map(reader, factor)
