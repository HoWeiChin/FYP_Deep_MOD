import matplotlib.pyplot as plt
import numpy as np
import sys
import re
import os
sys.path.append('/gpfs0/home/e0031794/Documents/DeePyMoD/src')
from deepymod.utilities import library_matrix_mat, print_PDE, tensorboard_to_dataframe

class SingleCostPlot:
    
    def plot_cost(self, data_frame, cost_plot_path):
    
        """
            data_frame (pandas df): pandas data frame generated from deepmod tf output
            cost_plot (str): file path of cost_plot with .png extension

        
        """
        fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(15,8.0))
    
        ax1.semilogy(data_frame['epoch'], data_frame['MSE_cost_0'], label='MSE')
        ax1.semilogy(data_frame['epoch'], data_frame['PI_cost_0'], label='Reg')
        ax1.semilogy(data_frame['epoch'], data_frame['L1_cost_0'], label=r'L$_1$')
        ax1.semilogy(data_frame['epoch'], data_frame['Total_cost_1'], label='Total cost')
        ax1.set(ylabel='Cost')
        ax1.set_xlabel('Epoch')
        ax1.legend(loc='best')
    
        plt.savefig(cost_plot_path)
    
class SingleCoeffPlot:

    def plot_coeff(self, data_frame, coeff_plot_path):
    
        """
            data_frame (pandas df): pandas data frame generated from deepmod tf output
            cost_plot (str): file path of cost_plot with .png extension
        
        """
        fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(15,8.0))
        u = ['1', 'u', 'u^2']
        du = ['1', 'u_{x}', 'u_{xx}', 'u_{xxx}']
        coeffs = library_matrix_mat(u, du)
        coeffs_terms = []
    
        for coeff_vec in np.array(data_frame['coeffs'].values):
            coeffs_terms.append(np.expand_dims(coeff_vec, axis=1))
        coeffs_np = np.array(coeffs_terms).squeeze()


        for i in np.arange(len(coeffs)):
            label = '$'+coeffs[i]+'$'
            line = ax1.plot(data_frame['epoch'], coeffs_np[:, i], label=label)

        ax1.set(xlabel=r'Epochs', ylabel='Coefficient')
        ax1.legend()
    
        plt.savefig(coeff_plot_path)
    
class SinglePlots:
    
    def __init__(self, event_path, save_path):
        self.event_path = event_path
        self.save_path = save_path
    
    def plot(self, target_file_name, cost_plot_name, coeff_plot_name):
        
        file = [file for file in os.listdir(self.event_path) if target_file_name in file][0]
        
        abs_file_path = os.path.join(self.event_path, file)
        data_frame = tensorboard_to_dataframe(abs_file_path)
    
        cost_plot_path = os.path.join(self.save_path, cost_plot_name)
        coeff_plot_path = os.path.join(self.save_path, coeff_plot_name)
    
        SingleCostPlot().plot_cost(data_frame, cost_plot_path)
        SingleCoeffPlot().plot_coeff(data_frame, coeff_plot_path)

if __name__ == "__main__":
    #example usage
    event_path = '/gpfs0/home/e0031794/Documents/FYP/FYP_results_11_9_2019/data_slicing/1_trial/tf_events_scaling'
    save_path = event_path
    sp = SinglePlots(event_path, save_path)
    sp.plot('0_subset', '0_cost.png', '0_coeff.png')