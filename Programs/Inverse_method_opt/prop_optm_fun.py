import os

def struc_prop(core_width, n_lam, plate_width, plate_height,t):
    var1 = "core_width = {}".format(core_width)
    var2 = "n_lam = {}".format(n_lam)
    var3 = "plate_width = {}".format(plate_width)
    var4 = "plate_height = {}".format(plate_height)
    var5 = "t = {}".format(t)
    struct_var = [var1,var2,var3,var4,var5]
    return struct_var

def mat_prop(array):
    G = array[5]/(2*(1+array[7]))
    var1 = "E1 = {}".format(array[0])
    var2 = "E2 = {}".format(array[1])
    var3 = "G12 = {}".format(array[2])
    var4 = "v12 = {}".format(array[3])
    var5 = "rho_g = {}".format(array[4])
    var6 = "E = {}".format(array[5])
    var7 = "v = {}".format(array[6])
    var8 = "G = {}".format(G)  
    var9 = "rho_r = {}".format(array[7])
    mat_var = [var1,var2,var3,var4,var5,var6,var7,var8,var9]
    return mat_var


def run_model(struct_var, mat_var):
    var_file = open("C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\Database\\Undamaged\\APDL_Und_Variables.txt","w")
    
    for i in struct_var:
        var_file.write(i)
        var_file.write('\n')
        
    for i in mat_var:
        var_file.write(i)
        var_file.write('\n')
        
    var_file.close()
    
    os.system("\"C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v212\\ansys\\bin\\winx64\\MAPDL.exe\" -b -j output -dir C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\ -i C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\\APDL_Undamaged.txt -o C:\\Users\\Ian\\Desktop\\Unifei\\GEMEC\\5_FEM\\Database\\Undamaged\\Model_Output.out")

