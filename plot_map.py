import csv
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plot
#from params import params

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
    alpha = np.zeros(combinations)

    i = 0
    for row in data:
        for col in row:
        #for col in row:
            pair = eval(col)
            colors[i] = float(pair[1]) # color for freq
            size = float(pair[0]) # size for ratio
            alpha[i] = nb_elts[i//std.shape[1],i%std.shape[1]]/nb_runs
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
    #mapper.set_clim(0.,20.)
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1, rotation='vertical')
    plot.yticks(p2)
    #plot.xlim([.0000001,.1]) # TODO: remove!!!! hack just to plot the TC param search
    for x,y,a,c,m,t in zip(axis1,axis2,area,colors,marks,alpha):
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none',alpha =t )
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
    axis1 = [ i for j in p2 for i in p1 ]
    axis2 = [ j for j in p2 for i in p1 ]
    combinations = len(p1) * len(p2)
    area = np.zeros(combinations)
    colors = np.zeros(combinations)
    marks = ['o' for i in range(combinations)]
    alpha = np.zeros(combinations)

    i = 0
    for row in data:
        for col in row:
            pair = eval(col)
            colors[i] = float(pair[1]) # color for f
            size = std[i//std.shape[1],i%std.shape[1]]+ 0.5 # size for std
            alpha[i] = 1 #nb_elts[i//std.shape[0],i%std.shape[0]]/nb_runs
            area[i] = size * factor
            i=i+1

    # normalize colors for matplotlib
    fig = plot.figure(1)
    norm = ml.colors.Normalize(vmin=min(colors), vmax=max(colors), clip=True)
    mapper = ml.cm.ScalarMappable(norm=norm, cmap=plot.cm.jet)
    mapper._A = [] # hack to plot the colorbar http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
    mapper.set_clim(vmin = 0.,vmax = 6.)
    plot.xlabel(text1)
    plot.ylabel(text2)
    plot.xticks(p1, rotation='vertical')
    plot.yticks(p2)
    #plot.xlim([.0000001,.1]) # TODO: remove!!!! hack just to plot the TC param search
    for x,y,a,c,m,t in zip(axis1,axis2,area,colors,marks,alpha):
        plot.scatter( x, y, s=a, c=mapper.to_rgba(c), marker=m, edgecolors='none',alpha=t)
    cbar = plot.colorbar(mapper)
    cbar.ax.set_ylabel('largest frequency', rotation=270)
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.tick_params(axis='both', which='minor', labelsize=8)
    plot.title('Averaged over '+str(nb_runs)+' trials')
    #plot.xscale('log') # TODO: remove!!!! hack just to plot the TC param search
    plot.savefig('var_map.png')
    fig.clear()



def push_effect_map(csvfile):

    data = list(csvfile)
    header1 = data.pop(0)[0]
    text1, p1 = header1.strip('#').split(':')
    header2 = data.pop(0)[0]
    text2, p2 = header2.strip('#').split(':')
    print data


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

    map = np.zeros((len(values1),len(values2)))
	
    for i,push_interval in enumerate(values1):
	for j, push_strength in enumerate(values2):
	    print eval(data[j][i])[1], 1000/push_interval
	    map[i,j] = eval(data[j][i])[1] - 1000/push_interval
	
    print map,values1,values2	
    fig = plot.imshow(map)
    plot.colorbar()
    plot.xlabel('push_interval')
    plot.ylabel('push_strength')
    #plot.xticks(values1)
    plot.yticks(values2)	
    plot.show()
    #fig.savefig('push_effect_map.png')

def mean_maps(nb_runs,path,key):
    for run in range(nb_runs):
        print run
        reader = csv.reader( open('/media/eloise/EC741CFE741CCCE8/results/' + path+str(run)+'/map-'+key+'.csv', 'rb') )
        data = list(reader)
        local_data = np.array([data[i] for i in range(2,len(data))])
        if run == 0:
            mean_data = data
            fqcy = np.zeros((local_data.shape[0],local_data.shape[1],nb_runs))
            nb_elts = np.zeros(local_data.shape)
        for i in range(len(local_data)):
            for j in range(len(local_data[i])):
                if run == 0:
                    mean_data[i+2][j] = np.array(eval(local_data[i][j])) * (np.array(eval(local_data[i][j]))[1]!=0)
                else:
                    #average only the ones that don't die out
                    mean_data[i+2][j] = mean_data[i+2][j] + np.array(eval(local_data[i][j]))*(np.array(eval(local_data[i][j]))[1]!=0)
                nb_elts[i,j] = nb_elts[i,j] + (np.array(eval(local_data[i][j]))[1]!=0)
                fqcy[i,j,run] = np.array(eval(local_data[i][j]))[1]
    
    for i in range(len(local_data)):
         for j in range(len(local_data[i])):
             mean_data[i+2][j] = (mean_data[i+2][j]/max(nb_elts[i,j],1)).tolist()

    if nb_runs > 1:
	std = np.std(fqcy,2)
    else:
	std = np.ones((fqcy.shape[0],fqcy.shape[1]))
     
    with open('/media/eloise/EC741CFE741CCCE8/results/'+ map_path+'0' + '/mean_map'+'.csv', 'wb') as csvfile:
        mywriter = csv.writer(csvfile)
        for row in range(len(mean_data)):
            mywriter.writerow(mean_data[row])

    return std, nb_elts



# using the function...
factor = 100
nb_runs = 7
#map_path = 'PushPy+Inh'	
map_path = 'long_run_pushPy+Inh'
#plot_map(reader, factor)
std,nb_elts = mean_maps(nb_runs,map_path,'inh')
reader = csv.reader( open('/media/eloise/EC741CFE741CCCE8/results/'+ map_path+'0'+'/mean_map.csv', 'rb') )
plot_var_map(reader,std,factor)
reader = csv.reader( open('/media/eloise/EC741CFE741CCCE8/results/'+map_path+'0'+'/mean_map.csv', 'rb') )
#plot_map(reader)
push_effect_map(reader)
