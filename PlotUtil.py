
path_to_deep_mod = '/gpfs0/home/e0031794/Documents/DeePyMoD/src'
import sys
sys.path.append(path_to_deep_mod)
#sys.path.append('/gpfs0/home/e0031794/Documents/FYP/FYP_results_11_9_2019/')

import matplotlib.pyplot as plt
import numpy as np
import os

from deepymod.utilities import library_matrix_mat, tensorboard_to_dataframe

def plot_cost(event_path, save_file_name):
    """
        event_path (str): path to events file which is produced during training
        save_file_name (str): full_path for file name to save diagram

    """
    data_frame = tensorboard_to_dataframe(event_path)
    fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(15, 8.0))

    ax1.semilogy(data_frame['epoch'], data_frame['MSE_cost_0'], label='MSE')
    ax1.semilogy(data_frame['epoch'], data_frame['PI_cost_0'], label='Reg')
    ax1.semilogy(data_frame['epoch'], data_frame['L1_cost_0'], label=r'L$_1$')
    ax1.semilogy(data_frame['epoch'], data_frame['Total_cost_1'], label='Total cost')
    ax1.set(ylabel='Cost')
    ax1.set_xlabel('Epoch')
    ax1.legend(loc='best')

    plt.savefig(save_file_name + '.png')

def plot_coeff(event_path, save_file_name):
    """
        event_path (str): path to events file which is produced during training
        save_file_name (str): full_path for file name to save diagram

    """
    data_frame = tensorboard_to_dataframe(event_path)
    fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(15, 8.0))

    u = ['1', 'u', 'uˆ2']
    du = ['1', 'u_{x}', 'u_{xx}', 'u_{xxx}']
    coeffs = library_matrix_mat(u, du)

    coeffs_list = []
    for coeff_vec in np.array(data_frame['coeffs'].values):
        coeffs_list.append(np.expand_dims(coeff_vec, axis=1))
    coeffs_np = np.array(coeffs_list).squeeze()

    for i in np.arange(len(coeffs)):
        if i == 0 :
            label_name = '$'+ coeffs[i] + '$'
        #print(label_name)
        #print('coeffs value', coeffs_np[:, i])
        ax1.plot(data_frame['epoch'], coeffs_np[:, i], label=label_name)
    ax1.set(xlabel=r'Epochs', ylabel='Coefficient')
    ax1.legend()

    plt.savefig(save_file_name + '.png')

def plot_all(event_path, save_name_cost, save_name_coeff):
    #os.chdir(event_dir)
    #event_path = [f for f in os.listdir() if '.mbi.' in f][0]
    #print('event_path', event_path)
    plot_cost(event_path, save_name_cost)
    plot_coeff(event_path, save_name_coeff)

if __name__ == "__main__":
    event_dir = "/gpfs0/home/e0031794/Documents/FYP/FYP_results_11_9_2019/output_diff_0.1_decay_3_14_12/20191216_091731/iteration_0"
    event_name = "events.out.tfevents.1576487854.bakkutteh"
    event_path = os.path.join(event_dir, event_name)

    output_cost = os.path.join(event_dir, 'cost')
    output_coeff = os.path.join(event_dir, 'coeff')

    plot_all(event_path, output_cost, output_coeff)


