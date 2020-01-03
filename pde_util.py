import sys
path_to_deep_mod = '/gpfs0/home/e0031794/Documents/DeePyMoD/src'
sys.path.append(path_to_deep_mod)

from deepymod.utilities import library_matrix_mat

class NormalTerm:

    """
        Stores non-derivative PDE terms

    """
    def __init__(self):
        self.u = ['1', 'u', 'uˆ2']
    
    def get_normal_terms(self):
        return self.u

class DerivativeTerm:

    """
        Stores non-derivative PDE terms

    """
    def __init__(self):
        self.du = ['1', 'u_{x}', 'u_{xx}', 'u_{xxx}']
    
    def get_derivative_terms(self):
        return self.du

class LibraryTerms:

    def __init__(self):
        self.normal_term = NormalTerm()
        self.derivative_term = DerivativeTerm()

    def get_library(self):

        """
            Gets a list of pde terms generated using cartersian product from terms originating from NormalTerm and DerivativeTerm.
            The list of pde terms is a library of basis terms.

        """

        normal_terms = self.normal_term.get_normal_terms()
        derivative_terms = self.derivative_term.get_derivative_terms()

        library = library_matrix_mat(normal_terms, derivative_terms)

        return library
    
    def get_library_len(self):
        library = self.get_library()
        return len(library)

class LibraryConfig:

    def get_library_config(self):

        """
            Gets configuration of pde library 
        """

        num_library_terms = LibraryTerms().get_library_len()

        library_config = {'total_terms': num_library_terms, 'deriv_order': 3, 'poly_order': 2}

        return library_config

class PDEManager:

    def get_lib_config_and_terms(self):
        lib_config = LibraryConfig().get_library_config()
        library = LibraryTerms().get_library()

        return lib_config, library

if __name__ == "__main__":
    config, lib = PDEManager().get_lib_config_and_terms()
    print(config)
    print(lib)


