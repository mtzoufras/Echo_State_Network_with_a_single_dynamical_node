#!/Users/mzoufras/anaconda/bin/python
# Developed by: Michail Tzoufras 

import numpy as np
import scipy 

import ast
import h5py

def Normal_weights(_X,_Y):
    return np.dot(  scipy.linalg.pinv(_X) , _Y)

def NRMSE(_Ybar,_Y):
    return np.sqrt(np.divide(
                     np.mean(np.square(_Y-_Ybar)),
                     np.var(_Y)))

def Augment_Sets(_X,_Y,_Bias,_lambda):
    
    __X = np.vstack([np.multiply(_Bias,np.ones(_X.shape[0]) ),_X.T]).T
    Reg = np.multiply(_lambda, np.eye(__X.shape[1]) )
    __X = np.vstack([__X, Reg])
    __Y = np.hstack([_Y, np.zeros(__X.shape[1])])
    
    return __X, __Y

def Read_N10_and_Oscillator(_N10,_Osc):
    with h5py.File(_N10, 'r') as N10_file, h5py.File(_Osc,'r') as Osc_File:
        return ast.literal_eval(N10_file.attrs['Header'] ), \
                 N10_file['Inputs'][:,:], \
                 N10_file['Outputs'][:,:], \
                 Osc_File['Oscillator Outputs'][:,:] 


def TrainData(_N10_File, _Oscillator_File, _training, _testing):

    print("Training...")
    
    N10, rInputs, rOutputs, Oscillator_Outputs = Read_N10_and_Oscillator(_N10_File,_Oscillator_File)

    Xtrain  = np.vstack( [ (Oscillator_Outputs[i,:]).reshape(N10['NElements'],N10['NThetas']) for i in _training ])
    _Ytrain = np.hstack([rOutputs[i,:] for i in _training ])

    Xtest  = np.vstack( [ (Oscillator_Outputs[i,:]).reshape(N10['NElements'],N10['NThetas']) for i in _testing ])
    _Ytest = np.hstack([ rOutputs[i,:] for i in _testing ])

#--------------
    #lambdas = [#1e-15,1e-16,1e-17,
    #            1e-18#,1e-19
    #]
    #thisC = [#0.1,0.01,
    #    1e-3#,1e-4,1e-5
    #]

    #NRMSE_best = 1.0
    #for ll in lambdas:
    #    for CC in thisC:
    #        Xtrain_a, _Ytrain_a = Augment_Sets(Xtrain,_Ytrain,CC,ll)
    #        Xtest_a, _Ytest_a = Augment_Sets(Xtest,_Ytest,CC,ll)
    #        weights = Normal_weights(Xtrain_a,_Ytrain_a)
    #        _Ybar_test  = np.dot(Xtest_a,weights.T)
    #        _Ybar_train = np.dot(Xtrain_a,weights.T)
    #        NRMSE_test = NRMSE(_Ybar_test,_Ytest_a)
    #        if NRMSE_test < NRMSE_best:
    #            lll, CCC = ll, CC
    #            NRMSE_best = NRMSE_test
    #            print str(ll) + "   " + str(CC) + "   "+ str(NRMSE_test)
#--------------

    lll = 1e-18
    CCC = 1e-3

    Xtrain_aug, Ytrain_aug = Augment_Sets(Xtrain,_Ytrain,CCC,lll)
    weights = Normal_weights(Xtrain_aug,Ytrain_aug)
    _Ybar_train = np.dot(Xtrain_aug,weights.T)
    _NRMSE_train = NRMSE(_Ybar_train,Ytrain_aug)

    Xtest_aug, Ytest_aug = Augment_Sets(Xtest,_Ytest,CCC,lll)
    _Ybar_test  = np.dot(Xtest_aug,weights.T)
    _NRMSE_test = NRMSE(_Ybar_test,Ytest_aug)

    return rInputs, _Ybar_train, _Ytrain, _NRMSE_train, _Ybar_test, _Ytest, _NRMSE_test 
