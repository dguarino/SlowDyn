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
            colors[i] = pair[0] # color for freq
            size = float(pair[1])
            # size for ratio
            # we want to be able to see whether the ratio is towards short-up, equal, or long-up
            # so we keep 0.5 where it is
            # and we raise the ratios below 0.5 with the same amount to bring it towards 1
            # 0.=1, 0.5=0.5, 1.=1
            if size < 0.5:
                size = size + (0.5-size)
                marks[i] = 's' # but we change their marker to diversify
            area[i] = size * factor
            i=i+1

    # normalize colors for matplotlib
    norm = ml.colors.Normalize(vmin=min(colors), vmax=max(colors), clip=True)
    mapper = plot.cm.ScalarMappable(norm=norm, cmap=plot.cm.jet)
    mapper._A = [] # hack to plot the colorbar http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1)
    plot.yticks(p2)
    for x,y,a,c,m in zip(axis1,axis2,area,colors,marks):
        #print x,y,a,c,m
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none')#, cmap=plot.cm.jet )
    plot.colorbar(mapper)
    plot.savefig('search_map.png')

# using the function...
factor = 100
reader = csv.reader( open('map.csv', 'rb') )
plot_map(reader, factor)
