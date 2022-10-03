# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os 

#with open(path, 'rb') as f:

    #data_temp = pickle.load(f)
    
#with open('resultado_otim.pickle', 'rb') as f:
    #a = pickle.load(f) 

import spyder_kernels

file_path = os.path.abspath('C:/Users/Ian/Desktop/Unifei/GEMEC/4_Programas/proprieties_optimization')
os.chdir(file_path)

data = spyder_kernels.utils.iofuncs.load_dictionary('resultado_otim.spydata')[0]

data['pos']

