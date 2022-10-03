import cluster_aux_fun_core as caf

if __name__ == '__main__': # This is used to run the script from cmd.
    struct_prop = (0.0125, 4, 0.2, 0.2)
    mat_prop = (20.7E9, 20.79E9, 4.5E9, 0.15, 2100, 92E6, 0.33, 20E6, 75)
    N = 1 # Start from N iteraration
    caf.run_cluster(struct_prop, mat_prop, N)