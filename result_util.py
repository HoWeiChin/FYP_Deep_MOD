import sys
path_to_deep_mod = '/gpfs0/home/e0031794/Documents/DeePyMoD/src'
sys.path.append(path_to_deep_mod)

from deepymod.utilities import print_PDE

class PdePrinter:

    def save_pde(self, sparse_vector, lib_terms, save_file):
        """
            sparse_vector (np array): sparse vector which is output from deepmod
            lib_terms (list): libary of pde basis terms 
            save_file (string): full path of file which a pde equation will be printed to

        """
        result = print_PDE(sparse_vector[0], lib_terms, PDE_term="u_t")
        with open(save_file, 'w+', encoding='utf-8') as f:
            f.write(result)

