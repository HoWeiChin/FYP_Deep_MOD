import sys
import pathlib
import numpy as np
import os

path_to_deep_mod = '/gpfs0/home/e0031794/Documents/DeePyMoD/src'
sys.path.append(path_to_deep_mod)

from deepymod.DeepMoD import DeepMoD
from deepymod.library_functions import library_1D
from parameters import ParamGetter
from pde_util import PDEManager
from result_util import PdePrinter
from gpu_util import GPUSetter

def pipeline(data_dir):
    #data_dir is an absolute path
    all_files_folders = os.listdir(data_dir)
    target_folders = [os.path.join(data_dir, obj) for obj in all_files_folders if '_subset' in obj] #search for subfolders

    #get all necessary configs
    lib_config, libary_terms = PDEManager().get_lib_config_and_terms()
    training_config, nn_layer_config = ParamGetter().get_trng_layer_params()
    output_config = {"output_directory": '', 'X_predict': ''}

    GPUSetter().set_max_gpu()

    #subset == amt of subset from original data. i.e amt of slicing done
    for folder in target_folders:

        if '.npy' in folder or '.txt' in folder:
            continue

        subset = folder.split('/')[-1].split('_')[0]  #get subset i.e 800, 900
                
        for_google_dir = os.path.join(folder + '/google_drive_storage') #we want to store relevant outputs in a folder and upload into google drive
        pathlib.Path(for_google_dir).mkdir(parents=True,exist_ok=True)
        
        full_x_t = np.load(os.path.join(folder, 'space_time_data_full_' + subset + '.npy'))
        x_t_train = np.load(os.path.join(folder, 'space_time_data_sampled_' + subset + '.npy'))
        bicoid_train = np.load(os.path.join(folder, 'bicoid_sampled_' + subset + '.npy'))
        
        save_dir =  os.path.join(folder, 'Out_subset_' + subset + '_expt')
        output_config['output_directory'] = save_dir
        output_config['X_predict'] = full_x_t

        sparse_vector, denoised = DeepMoD(
            x_t_train, bicoid_train, nn_layer_config,
            library_1D, lib_config, training_config, 
            output_config
            )

        #save results
        save_file_path = os.path.join(for_google_dir, 'pde_result_subset_' + subset + '.txt')
        PdePrinter().save_pde(sparse_vector, libary_terms, save_file_path)

        sparse_path = os.path.join(for_google_dir, 'sparse_vec_subset' + subset)
        denoised_path = os.path.join(for_google_dir, 'denoised_result_subset' + subset)

        #save training output and plots
        np.save(sparse_path, sparse_vector)
        np.save(denoised_path, denoised)

if __name__ == "__main__":
    pipeline('/gpfs0/home/e0031794/Documents/FYP/FYP_results_11_9_2019/data_slicing/1_trial')