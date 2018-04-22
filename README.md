# Reservoir computing with single dynamical node
In a 2011 article titled ["Information processing using a single dynamical node as complex system"](https://www.nature.com/articles/ncomms1476) L. Appeltant et al. showed that a nonlinear node with delayed feedback, such as a Mackey-Glass oscillator, can be used in lieu of a complex network in the paradigm of reservoir computing. The efficacy of their approach was confirmed through the NARMA10 benchmark: Four NARMA10 samples with length 800 points each, were preprocessed and fed through the single-node reservoir and the reservoir response was used for training and testing. A Normalized Root Mean Square Error (NMRSE) down to 0.12 (with twofold cross-validation) was achieved.

The present repository reproduces this result. It contains the following scripts: 
1. The `Narma10_Input.py` script generates a Narma10 file to be used as input for the single-node reservoir. This file contains the multiplexed 'masked' signals which are fed to the Mackey-Glass Oscillator(s). A `Narma10.h5` file that yields the desired cross-validation NMRSE = 0.12 is included. The `Narma10_Input.py` can be used to generate alternate Narma10 files.
2. The `MG_Oscillator.py` runs the Mackey-Glass simulation with the relevant input file. The oscillator response is saved in a file that is then used for training the network.
3. The `Training.py` script uses the Mackey-Glass oscillator response to train the network and calculate the NMRSE.
4. The `Visualization.py` script generates the figures shown here: (a) the response of the reservoir; (b) the fit on the training set and (c) the fit on the test set.
5. The `DynamicalNode_Reservoir.py` is a wrapper for the above scripts--the main program.

## Notes:

### on the Narma10 input
The binary masks used for multiplexing follow the guidance in [this (2014) paper](https://www.nature.com/articles/srep03629) by L. Appeltant et al.

### on the Mackey-Glass solver
The standard form of the Mackey-Glass equation is:

![first eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\frac{dx}{dt}&space;=&space;\beta&space;\frac{x(t-\tau)}{1&plus;[x(t-\tau)]^p}-\gamma&space;x(t),\quad\text{with}\quad\gamma,\beta,p>0)

This equation appears in [Appeltant](https://www.nature.com/articles/ncomms1476) with a different notation:

![second eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\dot{X}(t)=&space;-X(t)&plus;\frac{\eta\cdot[X(t-\tau)&plus;\zeta&space;J(t)]}{1&plus;[X(t-\tau)&plus;\zeta&space;J(t)]^p})

where clearly we recover the previous expression for:

![third_eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\gamma&space;=1,&space;\beta&space;=&space;\eta,\quad\text{and}&space;\quad&space;x(t-\tau)&space;\rightarrow&space;X(t-\tau)&plus;\zeta&space;J(t))

The method used for integrating this equation is the [implicit midpoint method](https://en.wikipedia.org/wiki/Midpoint_method):

![implicit midpoint](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\Bigl(1&plus;\frac{h}{2}\Bigr)X_{n&plus;1}=&space;\Bigl(1-\frac{h}{2}\Bigr)X_n&space;&plus;\frac{\eta\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]}{1&plus;\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]^p})

where _h_ is the timestep. To integrate a Delay Differential Equation (DDE) we need the values of _X_ at the present time _X(t)_ as well as its delayed value _X(t-&#964;)_. If _&#964;_ is an integral number _N_ of timesteps _h_, viz. if _&#964; = Nh_, then the value of _X(t-&#964;)_ has already been calculated and we can immediately substitute it in the equation above. Therefore we choose:

![timestep](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;h&space;=&space;\frac{2\tau}{2N&plus;1}\Rightarrow&space;t_n&plus;\frac{h}{2}-\tau&space;=&space;t_n-Nh)

_N_ represents the number of steps used to resolve the Delay Period _&#964;_.

### on the Mackey-Glass response

The response of the reservoir along with the input is shown for the normalized time interval [0,100]. The delay &#964; was chosen &#964; = 80 such that a transition at t = &#964; = 80 can be observed in the input signal from the first Narma10 value to the second. Each value from the Narma10 dataset is multiplexed through 400 virtual nodes with temporal distance	&#953; = &#964;/400 = 0.2. For an 800-long Narma10 signal the maximum normalized time is 800*80 = 64000.

![fig1](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Reservoir_Response.png?raw=true)

## on training

The fit is shown on the training set (samples 0 and 1). 
![fig2](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Train_Dataset.png?raw=true)

The fit is shown on the test set (samples 2 and 3).
![fig3](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Test_Dataset.png?raw=true)

Cross-validation is calculated by swapping the test and training datasets.
