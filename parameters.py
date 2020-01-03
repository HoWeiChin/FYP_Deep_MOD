class LayerParameter:

    """
        Stores parameters for DeepMod's architecture
        
    """

    def __init__(self):
        self.layers = {'layers': [2, 20, 20, 20, 20, 20, 1], 'lambda': 10e-6}
    
    def get_layers(self):
        return self.layers

class TrainingParameter:

    """
        Stores parameters for DeepMod's training

    """
    def __init__(self):
        self.training_param = {'max_iterations': 50000, 'grad_tol': 10**-6, 'learning_rate': 0.002, 'beta1': 0.99, 
        'beta2': 0.999, 'epsilon': 10 ** -8}
    
    def get_trng_config(self):
        return self.training_param

class ParamGetter:

    def get_trng_layer_params(self):
        return TrainingParameter().get_trng_config(), LayerParameter().get_layers()
        
if __name__ == "__main__":
    param_getter = ParamGetter()
    print(param_getter.get_trng_layer_params())