#!/Users/mzoufras/anaconda/bin/python
# Developed by: Michail Tzoufras 

import numpy as np
import scipy 
import ast
import h5py


class Temporal_Profile_MG(object):
        
    def __init__(self, _times, _values, _Simulation_Time, _h):
        
        self.Values = []
        time = 0.5*_h
        for i in range(1,len(_times)):
            while (time < _times[i]):
                (self.Values).append(_values[:,i-1])
                time += _h
        while (time < _Simulation_Time):
            self.Values.append(_values[:,-1])
            time += _h
        self.Values.append(_values[:,-1])

    def __call__(self,_step):
        return self.Values[_step]


class MackeyGlass(object):
    def __init__(self,_tau,_beta,_gamma,_p,_N):

        self.beta, self.gamma, self.p = _beta, _gamma, _p
        self.N, self.tau = _N, _tau
        self.h = 2.0*_tau/float(2*_N+1)
        self.y = [0.00001 for i in range(0,_N+1)] # Here we choose 2.0 as the initial value
    
    def run(self,_SimulationTime):
        """Run the simulation for a prescribed time without input."""
        Nmax = int(_SimulationTime/self.h)+len(self.y)
        Start = len(self.y)-1
        C1 = (1.0-0.5*self.gamma*self.h)
        invC2 = 1.0 /(1.0+0.5*self.gamma*self.h)
        for i in range(Start,Nmax):
            ynew = ( C1*self.y[i]+
                      self.beta*self.h*self.y[i-self.N]/(1.0+np.power(self.y[i-self.N],self.p))
                   )*invC2
            (self.y).append(ynew)
            
        return self.y[Start:]
    
    def run_driven(self,_SimulationTime,_zeta_J):
        """Run the several copies of the simulation for the given drivers z*J(t)."""
        
        Nmax = int(_SimulationTime/self.h)+len(self.y)
        Start = len(self.y)-1
        
        Y = np.zeros(( (_zeta_J(0)).size,Nmax-Start+1))
        Y[:,0] = self.y[Start]

        C1 = (1.0-0.5*self.gamma*self.h)
        invC2 = 1.0 /(1.0+0.5*self.gamma*self.h)
        
        for i in range(Start,Start+self.N+1):
            xt = self.y[i-self.N]+_zeta_J(i-Start)
            Y[:,i-Start+1] = ( C1*Y[:,i-Start]+
                             self.beta*self.h*xt*np.reciprocal(1.0+np.power(xt,self.p))
                           )*invC2

        for i in range(Start+self.N+1,Nmax):
            xt = Y[:,i-Start-self.N] + _zeta_J(i-Start)
            Y[:,i-Start+1] = ( C1*Y[:,i-Start]+
                           self.beta*self.h*xt*np.reciprocal(1.0+np.power(xt,self.p))
                           )*invC2
        return Y
    
    def Dt(self):
        return self.h
    
    def clear(self):
        """Clear the solver from previous values"""
        self.y = [0.01 for i in range(0,self.N+1)]
#-----------------------------------------------------------

def Oscillator_Simulation(_Filename, _Filename1):

    print("Running Mackey-Glass simulation...")

    with h5py.File(_Filename,'r') as rfile:
        N10 = ast.literal_eval(rfile.attrs['Header'] )
        Masked_N10 = rfile['Masked Inputs'][:,:]

    NumSteps = 2400 # This is the number of steps used to resolve one tau (delay time of the oscillator)
    Tau = 80.0
    Theta = Tau/np.float(N10['NThetas'] )
    Warmup_Time = 10000.0
    Cooldown_Time = 100.0
    Simulation_Time = N10['NElements']*Tau+Cooldown_Time

    MG = MackeyGlass(Tau, #tau
                 0.55,#beta/eta
                 1.0, #gamma (always 1)
                 1,   #p
                 NumSteps)

    zeta = 0.01
    Drivers = Temporal_Profile_MG(Theta * np.arange(Masked_N10.shape[1]), 
                               zeta*Masked_N10,
                               Simulation_Time,
                               MG.Dt())

    Warmup = MG.run(Warmup_Time) 
    Simulation = MG.run_driven(Simulation_Time,Drivers)

    MG_Output = np.zeros(Masked_N10.shape)
    for i in range(0,MG_Output.shape[1]):
        MG_Output[:,i] = Simulation[:, int(round( (i+1)*Theta/MG.Dt() ))]
    
    with h5py.File(_Filename1,'w') as ofile:
        ofile.create_dataset('Oscillator Outputs',data = MG_Output)

    return zeta*Masked_N10, Theta, Simulation, Simulation_Time
