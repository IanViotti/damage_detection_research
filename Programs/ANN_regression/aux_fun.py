import os 
import numpy as np
import pandas as pd

import shapely.affinity
from shapely.geometry import Point, Polygon

import matplotlib.pyplot as plt


def dam_num(file_name):
    try:
        dam_num = int(file_name.split('_')[0])
    except:
        dam_num = np.inf
    return dam_num

def get_skin_files():
    skin_var = pd.read_csv('skin_damage_variables.csv')
    os.chdir(os.path.join(os.getcwd(), 'skin_damage'))
    skin_files = os.listdir()
    return skin_files, skin_var

def get_skin_cls_data():
    skin_files, skin_var = get_skin_files()
    skin_files.sort(key = dam_num)

    skin_df = pd.DataFrame()

    for file in skin_files:
        if 'frequencias_naturais' in file:
            freq_file = pd.read_csv(file ,sep='\s+', skiprows=[1,2,3,4],
                           names=['SET','FREQ [Hz]', 'LOAD STEP', 'SUBSTEP', 'CUMULATIVE'] )
            freq_file = freq_file.drop(columns = ['LOAD STEP', 'SUBSTEP', 'CUMULATIVE', 'SET'])

            # Get damage number
            dam_number = file.split('_')[0] 

            # Rename column to damage number       
            freq_file = freq_file.rename(columns = {'FREQ [Hz]': f'Skin damage {dam_number}'}) 
            # Transpose df
            freq_file = freq_file.T 

            # Check if damage is in ply_num 1 (inter) or other ply (skin)
            if skin_var['n'][int(dam_number) - 1] == 1: 
                freq_file.insert(5, 'Type', 'Interface')
            else:
                freq_file.insert(5, 'Type', 'Skin')

            # Concatenate this model freqs to core_df
            skin_df = pd.concat([skin_df, freq_file], axis = 0) 
            
        if 'Mode' in file:
            mode += 1
                        
            mode_file = pd.read_csv(file, header = 0, index_col = False, 
                                    names=['Node Num', 'X', 'Y', 'Z', 'UX', 'UY', 'UZ'], sep='\s+')
            
            # Get UZ for selected nodes
            for i in range(len(get_nodes)):
                # Insert modes into dummy df
                freq_file.insert(15 + mode + i, f'UZ - N{i+1} M{mode}', [mode_file.loc[get_nodes[i]-1,'UZ']])
                                
            # Concat dummy df into main df
            
            # Get damage number
            
            # reset mode flag and mode_df 
            if mode == 4:
                skin_df = pd.concat([skin_df, freq_file], axis = 0) 
                mode_df = pd.DataFrame()
                mode = 0
        
        # Get only a few datapoint for testing
        if counter > 40 and test == True:
            break
    os.chdir('../')
    return skin_df

def get_skin_regr_data(get_nodes = (4814, 4788, 5711, 8351), test = False):
    
    # read damage parameters from .csv
    skin_var = pd.read_csv('skin_damage_variables.csv')
    
    # get into ../skin_damage dir
    os.chdir(os.path.join(os.getcwd(), 'skin_damage'))
    
    # list files in dir
    skin_files = os.listdir()
    
    # sort files list by damage number
    skin_files.sort(key = dam_num)
    
    # create dummy df
    skin_df = pd.DataFrame()
    mode_df = pd.DataFrame()
    
    # mode flag
    mode = 0 
    
    counter = 0
    
    for file in skin_files:
        counter += 1  
        # check if file is natural frequency
        if 'frequencias_naturais' in file:
            
            # read natural frequency file
            freq_file = pd.read_csv(file ,sep='\s+', skiprows=[1,2,3,4],
                           names=['SET','FREQ [Hz]', 'LOAD STEP', 'SUBSTEP', 'CUMULATIVE'] )
            
            freq_file = freq_file.drop(columns = ['LOAD STEP', 'SUBSTEP', 'CUMULATIVE', 'SET'])
            
            # Get damage number
            dam_number = file.split('_')[0] 

            # Rename column to damage number       
            freq_file = freq_file.rename(columns = {'FREQ [Hz]': f'Skin damage {dam_number}'}) 
            
            # Transpose df
            freq_file = freq_file.T 

            # Check if damage is in ply_num 1 (inter) or other ply (skin)
            if skin_var['n'][int(dam_number) - 1] == 1: 
                freq_file.insert(10, 'Type', 'Interface')
            else:
                freq_file.insert(10, 'Type', 'Skin')
    
            # manualy insert damage parameters to df
            freq_file.insert(11, 'pos x', skin_var['pos_x [m]'][int(dam_number) - 1])
            freq_file.insert(12, 'pos y', skin_var['pos_y [m]'][int(dam_number) - 1])
            freq_file.insert(13, 'theta', skin_var['theta [°]'][int(dam_number) - 1])
            freq_file.insert(14, 'c', skin_var['c [m]'][int(dam_number) - 1])
            freq_file.insert(15, 'r', skin_var['r [m/m]'][int(dam_number) - 1])
            
            #skin_df = pd.concat([skin_df, freq_file], axis = 0) 
        
        
        if 'Mode' in file:
            mode += 1
                        
            mode_file = pd.read_csv(file, header = 0, index_col = False, 
                                    names=['Node Num', 'X', 'Y', 'Z', 'UX', 'UY', 'UZ'], sep='\s+')
            
            # Get UZ for selected nodes
            for i in range(len(get_nodes)):
                # Insert modes into dummy df
                freq_file.insert(15 + mode + i, f'UZ - N{i+1} M{mode}', [mode_file.loc[get_nodes[i]-1,'UZ']])
                                
            # Concat dummy df into main df
            
            # Get damage number
            
            # reset mode flag and mode_df 
            if mode == 4:
                skin_df = pd.concat([skin_df, freq_file], axis = 0) 
                mode_df = pd.DataFrame()
                mode = 0
        
        # Get only a few datapoint for testing
        if counter > 40 and test == True:
            break
            
    # get back to main dir
    os.chdir('../')
    return skin_df

def get_core_files():
    os.chdir('../')
    core_var = pd.read_csv('core_damage_variables.csv')
    os.chdir(os.path.join(os.getcwd(), 'core_damage'))
    core_files = os.listdir()
    return core_files, core_var

def get_core_cls_data():
    core_files, core_var = get_core_files()
    core_files.sort(key = dam_num)

    core_df = pd.DataFrame()

    for file in core_files:
        if 'frequencias_naturais' in file:
            freq_file = pd.read_csv(file ,sep='\s+', skiprows=[1,2,3,4],
                           names=['SET','FREQ [Hz]', 'LOAD STEP', 'SUBSTEP', 'CUMULATIVE'] )
            freq_file = freq_file.drop(columns = ['LOAD STEP', 'SUBSTEP', 'CUMULATIVE', 'SET'])

            dam_number = file.split('_')[0] # Get damage number

            freq_file = freq_file.rename(columns = {'FREQ [Hz]': f'Core damage {dam_number}'}) # Rename column to damage number
            freq_file = freq_file.T # Transpose df

            freq_file.insert(5, 'Type', 'Core')

            core_df = pd.concat([core_df, freq_file], axis = 0) # Concatenate this model freqs to core_df
        
        if 'Mode' in file:
            mode += 1
                        
            mode_file = pd.read_csv(file, header = 0, index_col = False, 
                                    names=['Node Num', 'X', 'Y', 'Z', 'UX', 'UY', 'UZ'], sep='\s+')
            
            # Get UZ for selected nodes
            for i in range(len(get_nodes)):
                # Insert modes into dummy df
                freq_file.insert(16 + mode + i, f'UZ - N{i+1} M{mode}', [mode_file.loc[get_nodes[i]-1,'UZ']])
                                
            # Concat dummy df into main df
            
            # Get damage number
            
            # reset mode flag and mode_df 
            if mode == 4:
                core_df = pd.concat([core_df, freq_file], axis = 0) 
                mode_df = pd.DataFrame()
                mode = 0
        
        # Get only a few datapoint for testing
        if counter > 40 and test == True:
            break
            
    return core_df

def get_core_regr_data(get_nodes = (4814, 4788, 5711, 8351), test = False):
    
    # read damage parameters from .csv
    skin_var = pd.read_csv('core_damage_variables.csv')
    
    # get into ../skin_damage dir
    os.chdir(os.path.join(os.getcwd(), 'core_damage'))
    
    # list files in dir
    skin_files = os.listdir()
    
    # sort files list by damage number
    skin_files.sort(key = dam_num)
    
    # create dummy df
    core_df = pd.DataFrame()
    mode_df = pd.DataFrame()
    
    # mode flag
    mode = 0 
    
    counter = 0
    
    for file in skin_files:
        counter += 1  
        # check if file is natural frequency
        if 'frequencias_naturais' in file:
            
            # read natural frequency file
            freq_file = pd.read_csv(file ,sep='\s+', skiprows=[1,2,3,4],
                           names=['SET','FREQ [Hz]', 'LOAD STEP', 'SUBSTEP', 'CUMULATIVE'] )
            
            freq_file = freq_file.drop(columns = ['LOAD STEP', 'SUBSTEP', 'CUMULATIVE', 'SET'])
            
            # Get damage number
            dam_number = file.split('_')[0] 

            # Rename column to damage number       
            freq_file = freq_file.rename(columns = {'FREQ [Hz]': f'Core damage {dam_number}'}) 
            
            # Transpose df
            freq_file = freq_file.T 
    
            # manualy insert damage parameters to df
            freq_file.insert(10, 'pos x', skin_var['pos_x [m]'][int(dam_number) - 1])
            freq_file.insert(11, 'pos y', skin_var['pos_y [m]'][int(dam_number) - 1])
            freq_file.insert(12, 'theta_z', skin_var['theta_z [°]'][int(dam_number) - 1])
            freq_file.insert(13, 'c', skin_var['c [m]'][int(dam_number) - 1])
            freq_file.insert(14, 'r', skin_var['r [m/m]'][int(dam_number) - 1])
            freq_file.insert(15, 'pos_z', skin_var['pos_z [m]'][int(dam_number) - 1])
            freq_file.insert(16, 'theta_y', skin_var['theta_y [°]'][int(dam_number) - 1])        
        
        if 'Mode' in file:
            mode += 1
                        
            mode_file = pd.read_csv(file, header = 0, index_col = False, 
                                    names=['Node Num', 'X', 'Y', 'Z', 'UX', 'UY', 'UZ'], sep='\s+')
            
            # Get UZ for selected nodes
            for i in range(len(get_nodes)):
                # Insert modes into dummy df
                freq_file.insert(16 + mode + i, f'UZ - N{i+1} M{mode}', [mode_file.loc[get_nodes[i]-1,'UZ']])
                                
            # Concat dummy df into main df
            
            # Get damage number
            
            # reset mode flag and mode_df 
            if mode == 4:
                core_df = pd.concat([core_df, freq_file], axis = 0) 
                mode_df = pd.DataFrame()
                mode = 0
        
        # Get only a few datapoint for testing
        if counter > 40 and test == True:
            break
            
    # get back to main dir
    os.chdir('../')
    return core_df

def get_dam_cls_df():
    skin_df = get_skin_cls_data()
    core_df = get_core_cls_data()
    
    dam_df = pd.concat([core_df, skin_df])
    return dam_df

def plot_damage(dam_var, plate_x = 0.2, plate_y = 0.2, color = 'blue', **kwargs):
    '''Plots ellipse damage in plate for given damage variables and position limits if **kwargs == True'''
    
    min_bounds = kwargs.get('min_bounds')
    max_bounds = kwargs.get('max_bounds')
    
    pos_x = dam_var[0]
    pos_y = dam_var[1]
    theta = dam_var[2]
    c = dam_var[3]
    r = dam_var[4]
    
    # Rectangle definition
    polygon1 = Polygon([(0, 0),
       (plate_x, 0),
       (plate_x, plate_y),
       (0, plate_y),
    ])
    
    if min_bounds and max_bounds:
        polygon2 = Polygon([(min_bounds, min_bounds),
           (min_bounds, max_bounds),
           (max_bounds, max_bounds),
           (max_bounds, min_bounds),
        ])

    # Ellipse definition
    r_circ = 1
    circle = Point(pos_x, pos_y).buffer(r_circ)  # type(circle)=polygon
    ellipse1 = shapely.affinity.scale(circle, c/2, r*c/2)  # type(ellipse)=polygon
    ellipse = shapely.affinity.rotate(ellipse1, theta)

    # Plot
    plt.rcParams["figure.figsize"] = [6.00, 6.00]
    plt.rcParams["figure.autolayout"] = True


    xr1, yr1 = polygon1.exterior.xy
    if min_bounds and max_bounds:
        xr2, yr2 = polygon2.exterior.xy
    
    xe, ye = ellipse.exterior.xy
    plt.plot(xr1, yr1, c="green")
    if min_bounds and max_bounds:
        plt.plot(xr2, yr2, c="red")
    plt.plot(xe, ye, c=color)
    plt.title("Elliptical Damage in Plate")
    plt.grid()
    
    return 

def plot_damage2(dam_var, plate_z = 0.0125, plate_y = 0.2, color = 'blue', **kwargs):
    '''Plots ellipse damage in plate for given damage variables and position limits if **kwargs == True'''
    
    min_bounds = kwargs.get('min_bounds')
    max_bounds = kwargs.get('max_bounds')
    
    pos_z = dam_var[5]
    pos_y = dam_var[1]
    theta_z = dam_var[2]
    theta_y = dam_var[6]
    c = dam_var[3]
    r = dam_var[4]
    
    # Rectangle definition
    polygon1 = Polygon([(0, 0),
       (plate_z, 0),
       (plate_z, plate_y),
       (0, plate_y),
    ])
    
    if min_bounds and max_bounds:
        polygon2 = Polygon([(min_bounds, min_bounds),
           (min_bounds, max_bounds),
           (max_bounds, max_bounds),
           (max_bounds, min_bounds),
        ])

    # Ellipse definition
    r_circ = 1
    circle = Point(pos_z, pos_y).buffer(r_circ)  # type(circle)=polygon
    ellipse1 = shapely.affinity.scale(circle, r*c/2 , r*c/2*np.cos(np.radians(theta_z)) + c/2*np.sin(np.radians(theta_z)))  # type(ellipse)=polygon
    ellipse = shapely.affinity.rotate(ellipse1, theta_y)

    # Plot
    plt.rcParams["figure.figsize"] = [6.00*0.1, 6.00]
    plt.rcParams["figure.autolayout"] = True


    xr1, yr1 = polygon1.exterior.xy
    if min_bounds and max_bounds:
        xr2, yr2 = polygon2.exterior.xy
    
    xe, ye = ellipse.exterior.xy
    plt.plot(xr1, yr1, c="green")
    if min_bounds and max_bounds:
        plt.plot(xr2, yr2, c="red")
    plt.plot(xe, ye, c=color)
    #plt.title("Elliptical Damage in Plate")
    plt.grid()
    
    return 