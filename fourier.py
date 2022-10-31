# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 13:03:01 2022

@author: Francisco
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt5')
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

#%%

y=np.loadtxt("modo1_señal.csv")
t=np.loadtxt("modo1_tiempo.csv")

t=t-t[0] # hago una traslacion temporal para que empiece de 0
fs=10000 # frec de muestreo de esta medicion

# verifico que la frecuencia de muestreo sea la correcta
print(fs==round(1/(t[1]-t[0]),1)) 

# Decido en que rango quiero hacer la transformada

tin=0.1 # tiempo inicial en seg
tfin=0.799# tiempo final

t1=t[int(fs*tin):int(fs*tfin)]
y1=y[int(fs*tin):int(fs*tfin)]

plt.figure(2)
plt.plot(t,y,label="Datos")
plt.plot(t1,y1,label="Datos para Fourier")
plt.xlabel("Tiempo [s]",fontsize=13)
plt.ylabel("V",fontsize=13)
plt.axhline(y=np.mean(y),linestyle="--",color="red",label="valor medio")
plt.axvline(x=t[int(fs*tin)],linestyle="--",color="black")
plt.axvline(x=t[int(fs*tfin)],linestyle="--",color="black")
plt.grid()
plt.legend()
plt.show()

# Number of sample points
N = len(t1)
# sample spacing
T = (max(t1)-min(t1))/N
yf = fft(y1-np.mean(y)) # resto el valor medio para eliminar el pico en f=0
xf = fftfreq(N, T)[:N//2]
plt.figure(3)
plt.yscale('log')
plt.title("Transformada de Fourier de la perturbación",fontsize=13)
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),label="fft")  
plt.xlabel("f [Hz]",fontsize=13)
plt.ylabel("Amplitud",fontsize=13)
plt.grid()
plt.show()

