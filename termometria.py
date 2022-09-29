# -*- coding: utf-8 -*-
"""
@author: Francisco

Codigo para medir temperatura en funcion del tiempo con termocuplas tipo k,
usando voltimetros HEWLETT-PACKARD 34401A


"""

from __future__ import division, unicode_literals, print_function, absolute_import

import pyvisa as visa

import numpy as np
import matplotlib.pyplot as plt

import time

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt5')


plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

#%% Definición de funciones necesarias

"""
Definó una función que carga la tabla de calibración e interpola, permitiendo pasar
de voltaje (en mV) a temperatura (en K) y viceversa

Tabla de calibracion Termocupla tipo K:
Rango Temperatura: -200C a 500C (73K a 773K)
Rango Voltaje: -5.891 mV a 20.644 mV

"""

def TC_K_volt2temp_interp(mV): # en mV 
    data = np.loadtxt('termocupla_k_mv2T.csv',delimiter=',')
    temperature_vals = data[:,0] # en K 
    voltage_vals = data[:,1] # en mV 
    return np.interp(mV, voltage_vals, temperature_vals)

def TC_K_temp2volt_interp(T): # en K 
    data = np.loadtxt('termocupla_k_mv2T.csv',delimiter=',')
    temperature_vals = data[:,0] # en K 
    voltage_vals = data[:,1] # en mV 
    return np.interp(T, temperature_vals, voltage_vals)

"""
usando estas dos funciones calculo la temperatura que quiero medir, teniendo en 
consideración que las termocuplas estan calibradas a una referencia de 0 grados Celcius

sera necesario para esto medir temperatura ambiente con un termometro

"""

Tamb= 23.3 + 273.15 # T ambiente en Kelvin

def Texp(mVmedido):
    VoltCorregido=mVmedido+TC_K_temp2volt_interp(Tamb)
    Texp=TC_K_volt2temp_interp(VoltCorregido)
    return(Texp)


#%% Me conecto a los multimetros HEWLETT-PACKARD 34401A usando pyvisa

rm = visa.ResourceManager()

rm.list_resources()

resource_name1 = 'GPIB0::24::INSTR'
resource_name2 = 'GPIB0::23::INSTR'

mult1 = rm.open_resource(resource_name1)
mult2 = rm.open_resource(resource_name2)

# medición rapida de prueba

print("------mult1-------")
print(mult1.query('*IDN?'))
dc = float(mult1.query('MEASURE:VOLTAGE:DC?'))
print(r"V={dc} Volts".format(dc=dc))

print("T=",Texp(dc*1e3),"K")
print("T=",Texp(dc*1e3)-273.15,"C")

print("------mult2-------")
print(mult2.query('*IDN?'))
dc = float(mult2.query('MEASURE:VOLTAGE:DC?'))
print(r"V={dc} Volts".format(dc=dc))

print("T=",Texp(dc*1e3),"K")
print("T=",Texp(dc*1e3)-273.15,"C")

#%%  Medición en función del tiempo con dos termocuplas tipo k 

vmedido1=[] # lista para voltajes medidos en el multimetro 1 (en Volts)
y1=[] # lista para las temperaturas en K (mult1)

vmedido2=[] # lista para voltajes medidos en el multimetro 2 (en Volts)
y2=[] # lista para temperaturas en K (mult2)

t1=[] # tiempos de medicion del mult1
t2=[] # tiempos de medicion del mult2
t0=time.time()
for x in range(0,150,1):
    t2.append(time.time())
    dc2=float(mult2.query('MEASURE:VOLTAGE:DC?'))
    t1.append(time.time())
    dc1=float(mult1.query('MEASURE:VOLTAGE:DC?'))
    y2.append(Texp(dc2*1e3))
    y1.append(Texp(dc1*1e3))
    vmedido1.append(dc1)
    vmedido2.append(dc2)
    time.sleep(0.01)

t1=np.array(t1)-t0
t2=np.array(t2)-t0

plt.figure(1)
plt.title("Medición de temperatura con dos termocuplas k",fontsize=13)    
plt.plot(t1,np.array(y1)-273.15,".-.",label="Datos multi1")
plt.plot(t2,np.array(y2)-273.15,".-.",label="Datos multi2")
plt.plot((t2+t1)*1/2,-np.array(y2)+np.array(y1),".-.",label=r'$\Delta T$')
plt.ylabel(r'Temperatura [$^\circ$C]',fontsize=13)
plt.xlabel('Tiempo [s]',fontsize=13)
plt.legend(fontsize=13)
plt.tight_layout()
plt.grid(True)

