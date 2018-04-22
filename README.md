# Reservoir computing with single dynamical node
Demonstration of reservoir computing using a single dynamical node as described in https://www.nature.com/articles/ncomms1476

## The Mackey-Glass solver
The standard form of the Mackey-Glass equation is:

![first eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\frac{dx}{dt}&space;=&space;\beta&space;\frac{x(t-\tau)}{1&plus;[x(t-\tau)]^p}-\gamma&space;x(t),\quad\text{with}\quad\gamma,\beta,p>0)

This equation appears in [Appeltant](https://www.nature.com/articles/ncomms1476) with a different notation, as:

![second eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\dot{X}(t)=&space;-X(t)&plus;\frac{\eta\cdot[X(t-\tau)&plus;\zeta&space;J(t)]}{1&plus;[X(t-\tau)&plus;\zeta&space;J(t)]^p})

where clearly we recover the previous expression for:

![third_eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\gamma&space;=1,&space;\beta&space;=&space;\eta,\quad\text{and}&space;\quad&space;x(t-\tau)&space;\rightarrow&space;X(t-\tau)&plus;\zeta&space;J(t))

### Implicit midpoint method
Using the [implicit midpoint method](https://en.wikipedia.org/wiki/Midpoint_method):
![implicit midpoint](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\Bigl(1&plus;\frac{h}{2}\Bigr)X_{n&plus;1}=&space;\Bigl(1-\frac{h}{2}\Bigr)X_n&space;&plus;\frac{\eta\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]}{1&plus;\Bigl[X(t_n&plus;\frac{h}{2}-\tau)&plus;\zeta&space;J(t_n&plus;\frac{h}{2})\Bigr]^p})

Where _h_ is the time-step. With Delay Differential Equations we need the values of _X_ at the present time _t_ as well as its delayed value at _t-&#964;_. To avoid having to interpolate the time-step _h_ is chosen:

![timestep](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;h&space;=&space;\frac{2\tau}{2N&plus;1}\Rightarrow&space;t_n&plus;\frac{h}{2}-\tau&space;=&space;t_n-Nh)

Where _N_ is an integer number, the number of steps used to resolve the Delay Period _&#964;_. Finally, the values of the external driver--the multiplexed input _&#950;J(t)_ for which there is an analytical expression--can be defined at _t<sub>n</sub>+h/2_.

## Mackey-Glass oscillator output

![fig1](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Reservoir_Response.png?raw=true)

## Training sample output

![fig2](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Train_Dataset.png?raw=true)

![fig3](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Test_Dataset.png?raw=true)
