# -*- coding: utf-8 -*-
"""
Created on Mon May  9 10:58:25 2022

@author: Ian Viotti
"""

import pandas as pd
import numpy as np
import prop_optm_fun as fn
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history
import matplotlib.pyplot as plt
import time

# ================= Set model ======================
global_start_time = time.time() # set global timer

N = 4 # Number of frequencies to extract
freq_exc = 4 # Frequency to exclude

struct_var = fn.struc_prop(1.25E-2,4,0.19,0.2,0.25E-3) # (core width, number of plies, plate width, plate height, ply thickness)

w_exp = np.array([245.0, 475.0, 1185.0, 1672.0]) # Experimental values for natural frequencies

# ================= Model variables =================
# All variables must be in IS units
E1= 20.7E9
E2=20.7E9
G12=4.5E9
v12=0.15
rho_g=2100
E=92E6
v=0.43
rho_r = 75
mat_var_ar = np.array([E1,E2,G12,v12,rho_g,E,v,rho_r])

# ================= Optimization bounds ===================
var_range = 0.1 

max_bound = mat_var_ar*(1+var_range)
min_bound = mat_var_ar*(1-var_range)

bounds = (min_bound,max_bound)

# ================= Swarm initialization ===================
options = {'c1':2, 'c2': 2, 'w': 0.8} # c1: cognitive, c2: social, w: inertia

# ================= Set PSO ================================
particles_num = len(mat_var_ar)*10

optimizer = ps.single.GlobalBestPSO(n_particles=particles_num, dimensions=len(mat_var_ar), options=options, bounds=bounds, oh_strategy={"w":'exp_decay'})

# ================= Objective function =====================
partic = 0
it = 1

def obj_fun(mat_var_ar):
    
    global partic # Calls global partic and it variables (flags)
    global it
    
    F_w = []
    for i in mat_var_ar:
        start_time = time.time() # Timer

        mat_var = fn.mat_prop(i) # (E1,E2,G12,v12,rho_g,E,v,rho_r)
        
        fn.run_model(struct_var, mat_var) # run Ansys model with structure and materials variables
        
        partic += 1 # Uptate particle flag
        freq_file = pd.read_csv(r"C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\\frequencias_naturais.txt",sep='\s+', skiprows=[1,2,3,4],
                               names=['SET','FREQ [Hz]', 'LOAD STEP', 'SUBSTEP', 'CUMULATIVE'] )
        
        w_fem = np.delete(freq_file.to_numpy().T[1][0:(N+1)],freq_exc-1) # Extract the first N freq and exclude the freq_exc-th
        
        F_w_iter = [] # objective function (root mean square error of the particle)
        for j in range(N): 
            F_w_j = (w_fem[j]-w_exp[j])**2/N
            F_w_iter.append(F_w_j)
        F_w_iter = sum(F_w_iter)
        
        F_w.append(F_w_iter)
        
        it_timer = time.time() - start_time # Check Ansys run time
        
        print('===========================')
        print('\n== Iteration number: ', it)
        print('\n== Particle number: ', partic)
        print('\n== Run time: ', round(it_timer,2))
        print('\n== Particle freq: ', w_fem)
        print('\n== Cost function: ', F_w_iter)
        
    it += 1
    
    return F_w

# ================= Optimizer ==============================
cost, pos = optimizer.optimize(obj_fun, iters=2)

# ================= Post processing ==============================
global_timer = time.time() - global_start_time # Check Ansys run time

print('== Total run time: ', global_timer)

plot_cost_history(cost_history=optimizer.cost_history)
plt.show()