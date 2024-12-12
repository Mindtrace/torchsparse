import glob
import os

import torch
import torch.cuda
from setuptools import find_packages, setup
from torch.utils.cpp_extension import (CUDA_HOME, BuildExtension, CppExtension,
                                     CUDAExtension)

# Replace with direct version string
VERSION = '1.4.0'  # or whatever version you're using

if ((torch.cuda.is_available() and CUDA_HOME is not None)
        or (os.getenv('FORCE_CUDA', '0') == '1')):
    device = 'cuda'
else:
    device = 'cpu'

sources = [os.path.join('torchsparse', 'backend', f'pybind_{device}.cpp')]
for fpath in glob.glob(os.path.join('torchsparse', 'backend', '**', '*')):
    if ((fpath.endswith('_cpu.cpp') and device in ['cpu', 'cuda'])
            or (fpath.endswith('_cuda.cu') and device == 'cuda')):
        sources.append(fpath)

extension_type = CUDAExtension if device == 'cuda' else CppExtension
extra_compile_args = {
    'cxx': ['-g', '-O3', '-fopenmp', '-lgomp'],
    'nvcc': ['-O3']
}

setup(
    name='torchsparse',
    version=VERSION,  # Use the direct version string
    packages=find_packages(),
    ext_modules=[
        extension_type('torchsparse.backend',
                      sources,
                      extra_compile_args=extra_compile_args)
    ],
    cmdclass={'build_ext': BuildExtension},
    zip_safe=False,
    install_requires=[
        'torch>=1.7.0',
        'numpy>=1.20.0,<2.0.0',  # Add numpy constraint
    ],
    python_requires='>=3.7',
)
