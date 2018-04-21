#!/Users/mzoufras/anaconda/bin/python
# Developed by: Michail Tzoufras 

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white")

def Sample_n_Hold_Plot(_holds,_period,_end):
    """Starting from a list of points: create the corresponding piecewise-constant x- and y-axis data
    Return: piecewise x-axis-data, piecewise y-axis-data"""
    square_sig = []
    square_x = []
    for i in range(0,len(_holds)-1):
        square_x += [i*_period] + [(i+1)*_period]
        square_sig += [_holds[i]]*2
    square_x +=[(len(_holds)-1)*_period]+[_end]
    square_sig += [_holds[-1]]*2
    return square_x, square_sig


def Reservoir_Response(_Driver, _Theta, _Sim, _Sim_time, _FileName):
    Sample_to_plot = 0
    PC_x1, PC_y1 = Sample_n_Hold_Plot(_Driver[Sample_to_plot], _Theta, _Driver.shape[1]*_Theta)

    fig_osc, ax_osc = plt.subplots(figsize=(16, 4))
    Alltimes = _Sim_time/float(_Sim.shape[1]) * np.arange(_Sim.shape[1])
    ax_osc.set_title('Total simulation time = %.0f '%(_Driver.shape[1]*_Theta) , fontsize = 14, loc = 'right')
    ax_osc.plot(PC_x1, PC_y1, color = 'blue',lw=0.5, label = r'$\gamma \,J$'+'   (Input)')
    ax_osc.set_xlabel('Normalized Time',fontsize = 14)
    ax_osc.set_xlim(0,100)
    ax_osc.set_xticks([0,20,40,60,80,100])
    ax_osc.set_xticklabels([r'$0$',r'$20$',r'$40$',r'$60$',r'$80$',r'$100$'],fontsize = 14)
    ax_osc.plot(Alltimes,_Sim[Sample_to_plot,:], color = 'red', label = 'X    (Reservoir response)')
    ax_osc.legend(loc='lower left',bbox_to_anchor=(0.0, 0.94), shadow=True, ncol=2,fontsize = 16)

    fig_osc.savefig(_FileName, bbox_inches='tight')


def Trained_Datasets(_Inputs, _Ybar, _Y, _NRMSE, _samples, _title, _FileName):
    fig, ax = plt.subplots(len(_samples), 1, sharex=True, figsize=(16,8))
    ax[0].set_title( _title, fontsize = 20, loc='right')

    for i in range(0,len(_samples)):
        Ra = (i*_Inputs.shape[1],(i+1)*_Inputs.shape[1])
        ax[i].plot(_Inputs[_samples[i],:],color = 'grey',lw = 2, alpha = 0.3, label = r'$u_{sample,%d}$'%_samples[i])
        ax[i].plot(_Ybar[Ra[0]:Ra[1]], color = 'red', lw = 1,label = r'$\widehat{y}_{sample,%d}$'%_samples[i])
        ax[i].plot(_Y[Ra[0]:Ra[1]], color = 'blue', lw = 1,label = r'$y_{sample,%d}$'%_samples[i])
        ax[i].legend(loc='lower left',bbox_to_anchor=(0.0, 0.94), shadow=True, ncol=3,fontsize = 16)
        ax[i].set_ylim(0.0,1.0)

    fig.savefig(_FileName)