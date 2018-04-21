#!/Users/mzoufras/anaconda/bin/python
# Developed by: Michail Tzoufras 
import numpy as np
import os.path

import Narma10_Input
import Visualization as Vis
from MG_Oscillator import Oscillator_Simulation
from Training import TrainData

if (__name__=="__main__"):

#   Filenames
    NarmaFile, OscillatorFile = 'Narma10.h5','ReservoirResponse.h5'
    
#   Split between training and testing datasets
    training, testing = [0,1], [2,3]

#   Create Narma10 samples and the Multiplexed input data
    if not os.path.isfile( os.getcwd()+'/'+NarmaFile ):
        Narma10_Input.CreateSamples(NarmaFile, len(training)+len(testing) )
        if os.path.isfile( os.getcwd()+'/'+OscillatorFile ):
            os.remove( os.getcwd()+'/'+OscillatorFile )

#   Pass the Multiplexed input through the nonlinear node
    if not os.path.isfile( os.getcwd()+'/'+OscillatorFile ):
        Driver, Virtual_Node_time, Sim, Sim_time = Oscillator_Simulation(NarmaFile, OscillatorFile)  
        Vis.Reservoir_Response(Driver, Virtual_Node_time, Sim, Sim_time, 'Reservoir_Response.png')

#   Train 
    Inputs, Ybar_train, Ytrain, NRMSE_train, Ybar_test, Ytest, NRMSE_test1 = TrainData(NarmaFile, OscillatorFile, training, testing)

    Vis.Trained_Datasets(Inputs, Ybar_train, Ytrain, NRMSE_train, training, r'$NRMSE_{train} = %.3f$'%NRMSE_train, 'Train_Dataset.png')
    Vis.Trained_Datasets(Inputs, Ybar_test,   Ytest, NRMSE_test1,  testing, r'$NRMSE_{test} = %.3f$'%NRMSE_test1, 'Test_Dataset.png')

#   Flip training and testing datasets to calculate the 2-fold crossvalidation error
    Inputs, Ybar_train, Ytrain, NRMSE_train, Ybar_test, Ytest, NRMSE_test2 = TrainData(NarmaFile, OscillatorFile, testing, training)

    print('2-fold Cross-Validation NMRSE = %.2f'%(0.5*(NRMSE_test1 + NRMSE_test2)))