#Eugene m Izhikevich Model
import numpy as np
import random as rp
import matplotlib.pyplot as pylt

#for Excitatory neuron
Neuron_excit = 800
rand_ex = np.ones((Neuron_excit,1))

for _ in range(0,Neuron_excit):
    
    rand_ex[_,0] = rp.random()

a_e =  0.02*np.ones((Neuron_excit,1))
b_e =  0.2*np.ones((Neuron_excit,1))
c_e = -65 + 15*np.square(rand_ex)
d_e = 8 - + 6*np.square(rand_ex)

# for inhibitory neuron
Neuron_inhib = 200
rand_in = np.ones((Neuron_inhib,1))

def randn(Neuron_inhib):
    rando = np.ones((Neuron_inhib,1))
    for _ in range(0,Neuron_inhib):
        
        rando[_,0] = rp.random()
    return rando

a_i = 0.02 + 0.08*rand_in
b_i = 0.25-0.05*rand_in
c_i = -65*np.ones((Neuron_inhib,1))
d_i = 2*np.ones((Neuron_inhib,1))

#weight
s1 = np.ones((Neuron_excit,Neuron_excit))
for _ in range(0,Neuron_excit):
    for k in range(0,Neuron_excit):
        s1[_,k] = rp.random()
        
s2 = np.ones((Neuron_inhib,Neuron_inhib))
for p in range(0,Neuron_inhib):
    for q in range(0,Neuron_inhib):
        s1[p,q] = rp.random()



a =np.concatenate((a_e,a_i))
b =np.concatenate((b_e,b_i))
c =np.concatenate((c_e,c_i))
d =np.concatenate((d_e,d_i))


#initial value of V
v = -65*np.ones((Neuron_excit+Neuron_inhib,1))
#initial value of u
u = np.multiply(b,v)


### Setting running time
time = np.ones((1000,1))
for i in range(0,1000):
    time[i,0]=i
##record
firings = np.zeros((Neuron_excit+Neuron_inhib,len(time)))

# running sim
for t in range(len(time)):
    
    # Thalamic Input
    I1 = 5*randn(Neuron_excit)
    I2 = 2*randn(Neuron_inhib)
    fired = []
    for _ in range(0,Neuron_excit+Neuron_inhib):
        if v[_] >= 30:
            fired.append(_)
    for _ in range(0,Neuron_excit+Neuron_inhib):
        if _ in fired:
            firings[_,t] = _
        else:
            firings[_,t] = 0
    for _ in range(len(fired)):
        v[_] = c [_]
        u[_] = u[_] + d[_]
    for _ in range(0,Neuron_excit+Neuron_inhib):
         
        if _<800:
            I1[:,0] = I1[:,0] + s1[:,_]+2
        elif _>=800:
            I2[:,0] = I2[:,0] + s2[:,abs(800-_)]+2
        
        I = np.concatenate((I1,I2))
        for _ in range(len(v)):
            v[_] = v[_] + 0.5*(0.04*np.square(v[_])+140-u[_]+I[_])
            v[_] = v[_] + 0.5*(0.04*np.square(v[_])+140-u[_]+I[_])
    
    u = u + np.multiply(a,(np.multiply(b,v) - u))
    
    
pylt.plot(firings,'.')      
    
    







