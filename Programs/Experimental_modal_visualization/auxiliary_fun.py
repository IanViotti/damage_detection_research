import os
from bisect import bisect

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy import interpolate
import numpy as np
import pandas as pd

def read_ImFRF(plate):
    path = os.path.abspath(os.path.join(os.getcwd(), '../../'))
    plate_dir = os.path.join(path, '7 - Experimental', plate, 'novos')
    data_files = os.listdir(plate_dir)
        
    ImFRF = []
    for file in data_files:
        if 'Im' in file:
            data_xlsx = pd.read_excel(os.path.join(plate_dir, f'{file}'))
            data_np = data_xlsx.to_numpy()
            ImFRF.append(data_np)            
    
    return ImFRF

def get_amplitude(Im_FRF, w_exp, n_points, rows, mode):
    A_imfrf_list = []
    for point in Im_FRF:
        for i in w_exp:
            X = bisect(point.T[0], i)
            Y = point.T[1][X]
            A_imfrf_list.append(Y)

    # to correctely arrange the rows and collumns
    amplitude_array = np.array(np.array_split(np.array(A_imfrf_list),n_points))
    
    # Extract amplitude for given mode
    mode_ImFRF = np.array_split(amplitude_array.T[mode - 1], rows)
    
    # Insert fixed nodes 
    columns = int(n_points / rows)
    fixed_nodes = np.zeros(columns)
    complete_mode_ImFRF = np.vstack((mode_ImFRF, fixed_nodes))
    
    return complete_mode_ImFRF

def plot_mode(node_im, refinement = None):
    # Creating dataset
    X = np.arange(0, np.shape(node_im)[0])
    Y = np.arange(0, np.shape(node_im)[1])
    X, Y = np.meshgrid(X, Y)
    Z = node_im
        
    xnew, ynew = np.mgrid[1: np.shape(node_im)[0] + 1:80j, 1 : np.shape(node_im)[1] + 1:80j]
    tck = interpolate.bisplrep(X, Y, Z, s=0)
    znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)    
    
    # Creating figure
    fig = plt.figure(figsize =(7, 6))
    ax = plt.axes(projection ='3d')

    # Creating color map
    my_cmap = plt.get_cmap('plasma')

    # Creating plot
    surf = ax.plot_surface(xnew, ynew, znew[::-1],
                           cmap = my_cmap,
                           edgecolor ='none')

    fig.colorbar(surf, ax = ax,
                 shrink = 0.5, aspect = 5)

    ax.set_title('Plate Modal Representation')
    ax.set_xlabel('X Nodes')
    ax.set_ylabel('Y Nodes')
    ax.set_zlabel('Im FRF [m/s/N]')
    
    ax.view_init(-140, 110)
    
    fig.savefig('Exp_mode_n.jpg', dpi = 500)
    
    # show plot
    #plt.show()