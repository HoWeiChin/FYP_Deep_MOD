import numpy as np
import os
import subprocess

class GPUGetter:

    def get_free_gpu(self):

        """
            Selects the gpu with the most free memory

        """
        output = subprocess.Popen('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free', stdout=subprocess.PIPE,
                              shell=True).communicate()[0]
        output = output.decode("ascii")

        # assumes that it is on the popiah server and the last gpu is not used
        memory_available = [int(x.split()[2]) for x in output.split("\n")[:-2]]

        if memory_available:
            print("Setting GPU to use to PID {}".format(np.argmax(memory_available)))
            return np.argmax(memory_available)

        if not memory_available:
            print('No GPU memory available')

class GPUSetter:

    def set_max_gpu(self):

        """
            Sets GPU with maximum memory

        """
        gpu_getter = GPUGetter()
        gpu = str(gpu_getter.get_free_gpu())

        if gpu:
            print("Using GPU: %s" % gpu)
            os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
            os.environ['CUDA_VISIBLE_DEVICES'] = gpu

        if not gpu:
            print('No GPU detected')

if __name__ == "__main__":
    """
        Example usage
    """
    gpu_setter = GPUSetter()
    gpu_setter.set_max_gpu()
