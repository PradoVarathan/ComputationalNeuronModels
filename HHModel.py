# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:01:00 2018

@author: Pradeep
"""

###################################
import numpy as np
import scipy 
from scipy.integrate import odeint
###################################
#setting up currents#
#  C*dV/dt = Ina+Ik+Il+Iapp
gNa = 1.20
gK = 0.36
gL = 0.003

E_l = -54.387
E_k = -77

E_na =50
I_stim = 0.06775

Cap = 0.01
t = np.linspace(0,100,100000)
# for leak
def I_leak(V):
    return gL*(V- E_l)
# for Na
def a_m(V):
    return 0.1*(V+40)*(1/(1-np.exp(-(V+40)/10)))
def b_m(V):
    return 4*np.exp(-0.0556*(V+65))
#for h
def a_h(V):
    return 0.07*np.exp((V+65)*-0.05)
def b_h(V):
    return 1/(np.exp(-0.1*(V+35))+1)
def a_n(V):
    return 0.01*(V+55)*(1/(1-np.exp(-(V+55)/10)))
def b_n(V):
    return 0.125*np.exp(-(V+65)/80)
def ingd(dts,t):
    V=dts[0]
    n=dts[1]
    m=dts[2]
    h=dts[3]
    digi = np.zeros((4,))
    
    def g_K(V,n):
        return gK*np.power(n,4)
    def g_Na(V,m,h):
        return gNa*np.power(m,3)*h
    
    digi[0]= (g_Na(V,m,h)*(E_na - V) + g_K(V,n)*(E_k - V) + I_leak(V) + I_stim)/Cap
    digi[1]= (a_n(V)*(1-n))-(b_n(V)*n)
    digi[2]= (a_m(V)*(1-m))-(b_m(V)*m)
    digi[3]= (a_h(V)*(1-h))-(b_h(V)*h)
    
    return digi



ivals = np.array([-64.9964,0.3177,0.053,0.596])

Comp = odeint(ingd,ivals,t)

Volt = Comp[:,0]

import matplotlib.pyplot as plt
plt.figure()
plt.plot(t,Volt)
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')
plt.show()
plt.subplot(3,1,1)
plt.plot(t,Comp[:,1])
plt.xlabel('Time [ms]')
plt.ylabel('Variable N')
plt.subplot(3,1,2)
plt.plot(t,Comp [:,2])
plt.xlabel('Time [ms]')
plt.ylabel('Variable M')
plt.subplot(3,1,3)
plt.plot(t,Comp [:,3])
plt.xlabel('Time [ms]')
plt.ylabel('Variable H')

app_time = []
for _ in range(1,len(t)):
    if Volt[_ - 1]<Volt[_]>Volt[_+1]:
        app_time.append(_)
    else:
        pass
print(app_time)

fir_freq = 1000*(len(app_time)/t[-1])
print("Firing frequency of the neuron is {} AP/s".format(fir_freq))
