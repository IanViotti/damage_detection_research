# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 18:43:59 2022

@author: Ian
"""

import os

#%%  Structure Variables
core_width = "core_width = 0.01"
n_lam = "n_lam = 5" # numero de camadas
plate_width = "plate_width = 0.2"
plate_height = "plate_height = 0.3"
struct_var = [core_width,n_lam,plate_width,plate_height]

# Skin Damage Variables
pos_x1 = "pos_x = 0.1"
pos_y1 = "pos_y = 0.15"
theta1 = "theta = 45"
c1 = "c = 0.05" # Elipse lenght
r1 = "r = 0.1" # Elipse lenth to width ratio 
n_dam1 = "n_dam = 2" # number of the damaged laminae (from the outter to the inner)
skin_var = struct_var + [pos_x1,pos_y1,theta1,c1,r1,n_dam1]

# Interface Damage Variables

pos_x2 = "pos_x = 0.1"
pos_y2 = "pos_y = 0.15"
theta2 = "theta = 45"
c2 = "c = 0.05" # Elipse lenght
r2 = "r = 0.1" # Elipse lenth to width ratio 
n_dam2 = "n_dam = n_lam" # number of the damaged laminae (from the outter to the inner)
inter_var = struct_var + [pos_x2,pos_y2,theta2,c2,r2,n_dam2]

# Core Damage Variables
pos_x3 = "pos_x = 0.1"
pos_y3 = "pos_y = 0.15"
pos_z3 = "pos_z = 0.005"
theta_x3 = "theta_x = 0"
theta_y3 = "theta_y = 0"
theta_z3 = "theta_z = 45"
c3 = "c = 0.02" # Elipsoid lenght
r3 = "r = 0.20" # Elipsoid width to length ratio 
core_var = struct_var + [pos_x3,pos_y3,pos_z3,theta_x3,theta_y3,theta_z3,c3,r3]

#%% dam_type: 0=Undamaged; 1=Skin Damage; 2=Interface Damage; 3=Core Damage 
dam_type = 0

if dam_type == 0:
    var_file = open("C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\Database\\Undamaged\\APDL_Und_Variables.txt","w")
    for i in struct_var:
        var_file.write(i)
        var_file.write('\n')
    var_file.close()
    
    os.system("\"C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v212\\ansys\\bin\\winx64\\MAPDL.exe\" -b -j output -dir C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\ -i C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\\APDL_Undamaged.txt -o C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\\Model_Output.out")

elif dam_type == 1:
    var_file = open("C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\Database\\Skin_Damage\\APDL_Skin_Variables.txt","w")
    for i in skin_var:
        var_file.write(i)
        var_file.write('\n')
    var_file.close()
    
    os.system("\"C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v212\\ansys\\bin\\winx64\\MAPDL.exe\" -b -j output -dir C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Skin_Damage\ -i C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Skin_Damage\\APDL_Skin_Damage.txt -o C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Skin_Damage\\Model_Output.out")
    
elif dam_type == 2:
    var_file = open("C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\Database\\Interface_Damage\\APDL_Inter_Variables.txt","w")
    for i in inter_var:
        var_file.write(i)
        var_file.write('\n')
    var_file.close()
    
    os.system("\"C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v212\\ansys\\bin\\winx64\\MAPDL.exe\" -b -j output -dir C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Interface_Damage\ -i C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Interface_Damage\\APDL_Inter_Damage.txt -o C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Interface_Damage\\Model_Output.out")
    
elif dam_type == 3:
    var_file = open("C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\Database\\Core_Damage\\APDL_Core_Variables.txt","w")
    for i in core_var:
        var_file.write(i)
        var_file.write('\n')
    var_file.close()
    
    os.system("\"C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v212\\ansys\\bin\\winx64\\MAPDL.exe\" -b -j output -dir C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Core_Damage\ -i C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Core_Damage\\APDL_Core_Damage.txt -o C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Core_Damage\\Model_Output.out")

else: 
    print('\n == Non valid dam_type ==')