# Reservoir computing with single dynamical node
In an article titled ["Information processing using a single dynamical node as complex system"](https://www.nature.com/articles/ncomms1476) L. Appeltant et al. showed that a nonlinear node with delayed feedback, such as a Mackey-Glass oscillator, can be used in lieu of a complex network in the paradigm of reservoir computing. The efficacy of their approach through the NARMA10 benchmark: 4 NARMA10 samples with length 800 points each were used and NRMSE down to 0.12 with twofold crossvalidation was obtained.

This repository reproduces this result. It contains the following scripts: 
1. The `Narma10_Input.py` file generates a Narma10 input file for the single-node reservoir. The file it generates includes a multiplexed 'masked' signal to be used by the Oscillator. Such a `Narma10.h5` file that yields the desired cross-validation NMRSE = 0.12 is included. The `Narma10_Input.py` can be used to generate alternate Narma10 files.
2. The `MG_Oscillator.py` runs the Mackey-Glass oscillator with the relevant input file. Its output is saved in a file that is then used for training the network.
3. The `Training.py` script uses the Mackey-Glass oscillator response to train the network and calculate the NMRSE.
4. The `Visualization.py` script is used to generate the figures shown here: (a) A figure that shows the response of the reservoir. (b) a figure that shows the prediction on the training set and (c) a figure that shows the prediction on the test set.
5. The `DynamicalNode_Reservoir.py` is the main program.

**_A few notes:_**

## on the Narma10 input
The binary masks used for multiplexing follow the guidance in [this paper](https://www.nature.com/articles/srep03629) by L. Appeltant et al.

## on the Mackey-Glass solver
The standard form of the Mackey-Glass equation is:

![first eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\frac{dx}{dt}&space;=&space;\beta&space;\frac{x(t-\tau)}{1&plus;[x(t-\tau)]^p}-\gamma&space;x(t),\quad\text{with}\quad\gamma,\beta,p>0)

This equation appears in [Appeltant](https://www.nature.com/articles/ncomms1476) with a different notation, as:

![second eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\dot{X}(t)=&space;-X(t)&plus;\frac{\eta\cdot[X(t-\tau)&plus;\zeta&space;J(t)]}{1&plus;[X(t-\tau)&plus;\zeta&space;J(t)]^p})

where clearly we recover the previous expression for:

![third_eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\gamma&space;=1,&space;\beta&space;=&space;\eta,\quad\text{and}&space;\quad&space;x(t-\tau)&space;\rightarrow&space;X(t-\tau)&plus;\zeta&space;J(t))

The method used for integrating this equation is described below: 

#### Implicit midpoint method
Using the [implicit midpoint method](https://en.wikipedia.org/wiki/Midpoint_method):

![implicit midpoint](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\Bigl(1&plus;\frac{h}{2}\Bigr)X_{n&plus;1}=&space;\Bigl(1-\frac{h}{2}\Bigr)X_n&space;&plus;\frac{\eta\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]}{1&plus;\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]^p})

Where _h_ is the time-step. With Delay Differential Equations (DDEs) we need the values of _X_ at the present time _t_ as well as its delayed value at _t-&#964;_. To avoid having to interpolate we can choose the time-step _h_ as:

![timestep](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;h&space;=&space;\frac{2\tau}{2N&plus;1}\Rightarrow&space;t_n&plus;\frac{h}{2}-\tau&space;=&space;t_n-Nh)

Where _N_ is an integer number: the number of steps used to resolve the Delay Period _&#964;_. Finally, the values of the external driver--the multiplexed input _&#950;J(t)_ for which there is an analytical expression--can be defined at _t<sub>n</sub>+h/2_.

## on the Mackey-Glass response

The response of the reservoir along with the input is shown up to normalized time t = 100. The Delay &#964; was chosen &#964; = 80 and 400 virtual nodes are used such that this figure shows a transition at t = &#964; = 80 from the first input Narma10 value to the second.
![fig1](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Reservoir_Response.png?raw=true)

## on training

The predition is shown on the training data, here samples 0 and 1.
![fig2](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Train_Dataset.png?raw=true)

The predition is shown on the test data, here samples 2 and 3.
![fig3](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Test_Dataset.png?raw=true)

Crossvalidation is calculated by swapping the test and training datasets. This is not shown here.
