#!/Users/mzoufras/anaconda/bin/python
# Developed by: Michail Tzoufras 

import numpy as np
from scipy.signal import max_len_seq
import ast
import h5py


def NARMA10(N):
    """
    Description:    Build a NARMA10 Dataset
    Usage:          builtNARMA10(N)
    Input:
        N       = number of values
    Output:
        u       = input values
        y       = function values
    """

    while True:
        # generate input
        u = 0.5 * np.random.uniform(low=0.0, high=1.0, size=(N+1000))

        # generate output arrays
        y_base = np.zeros(shape=(N+1000))

        # calculate intermediate output
        for i in range(10, N+1000):
            # implementation of a tenth order system model
            y_base[i] = 0.3 * y_base[i-1] + 0.05 * y_base[i-1] * \
                np.sum(y_base[i-10:i]) + 1.5 * u[i-1] * u[i-10] + 0.1

        if np.isfinite(y_base).all():
            return u[1000:], y_base[1000:]

        # otherwise, try again. You random numbers were unlucky
        else:
            print('Retry...')


def CreateSamples(_Filename, _NSamples):

    print("Creating Narma10 samples...")

    N10_Params = {}

    N10_Params['NSamples'] = _NSamples
    N10_Params['NElements'] = 800
    N10_Params['NThetas'] = 400

    # Narma10 I/O
    Inputs = np.zeros((N10_Params['NSamples'],N10_Params['NElements'] ))
    Outputs = np.zeros((N10_Params['NSamples'],N10_Params['NElements'] ))
    for i in range(0,N10_Params['NSamples']):    
        Inputs[i,:],Outputs[i,:] = NARMA10(N10_Params['NElements'] )

    # Mask: Use the Maximum Length Sequence with N > Number of Thetas
    MLS_word = np.int(np.log(N10_Params['NThetas'])/np.log(2))
    Preprocessing_Mask = 2.0*( np.hstack([ max_len_seq(MLS_word)[0],
                                       max_len_seq(MLS_word+1)[0] ] ) [:N10_Params['NThetas']]) - 1 
    Preprocessing_Mask *=0.1

    # Masked Inputs
    Masked_Inputs = np.zeros((N10_Params['NSamples'],N10_Params['NElements']*N10_Params['NThetas'] ))
    for i in range(0,N10_Params['NSamples']):
        for j in range(N10_Params['NElements'] ):
            Masked_Inputs[i,(j*N10_Params['NThetas'] ):(j+1)*N10_Params['NThetas'] 
                     ] = np.multiply(Inputs[i,j],Preprocessing_Mask) 

    with h5py.File(_Filename,'w') as ofile:
        ofile.attrs['Header'] = str(N10_Params)
        ofile.create_dataset('Inputs',data = Inputs)
        ofile.create_dataset('Outputs',data = Outputs)
        ofile.create_dataset('Mask',data = Preprocessing_Mask)
        ofile.create_dataset('Masked Inputs',data = Masked_Inputs)  

    return None       

