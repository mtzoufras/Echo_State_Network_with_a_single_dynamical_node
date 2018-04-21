# Reservoir computing with single dynamical node
Demonstration of reservoir computing using a single dynamical node as described in https://www.nature.com/articles/ncomms1476


The standard form of the Mackey-Glass equation is:

![first eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\frac{dx}{dt}&space;=&space;\beta&space;\frac{x(t-\tau)}{1&plus;[x(t-\tau)]^p}-\gamma&space;x(t),\quad\text{with}\quad\gamma,\beta,p>0)

The one implemented by Appeltant is:

![second eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\dot{X}(t)=&space;-X(t)&plus;\frac{\eta\cdot[X(t-\tau)&plus;\zeta&space;J(t)]}{1&plus;[X(t-\tau)&plus;\zeta&space;J(t)]^p})

Clearly:

![third_eq](https://latex.codecogs.com/gif.latex?\bg_white&space;\large&space;\gamma&space;=1,&space;\beta&space;=&space;\eta,\quad\text{and}&space;\quad&space;x(t-\tau)&space;\rightarrow&space;X(t-\tau)&plus;\zeta&space;J(t))

We need the temporal profile 	_&#950;J(t)_ and then we need its values at _&#950;J(t<sub>n</sub>+h/2)_.

![fig1](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Reservoir_Response.png?raw=true)

![fig2](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Train_Dataset.png?raw=true)

![fig3](https://github.com/mtzoufras/Reservoir_computing_with_a_single_dynamical_node/blob/master/Test_Dataset.png?raw=true)
