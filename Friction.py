import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

data=pd.read_excel(r"C:\Users\jonat\OneDrive\Documents\University\Year 2 Semester 2\PR48_data1.xlsx", sheet_name= "I = 0.0470")
xdata=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
ydata=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
for i in range(len(xdata)):
    xdata[i]=data["T"+str(i+1)+"(s)"]
    xdata[i]=xdata[i].dropna()
    ydata[i]=data["R"+str(i+1)]
    ydata[i] = np.log((2 * np.pi * (ydata[i])) / 16 / 60)
    ydata[i] = ydata[i].replace(-np.inf, 0)
    ydata[i]=ydata[i].dropna()


print(xdata)
print(ydata)
# define constants in S.I
electrical_conductivity=2.73e7
magnet_turns=250  # Fix me with a calculator
disk_thickness=2e-3
pole_area=2.828e-3
pole_disk_distance=70e-3
B=24.16e-3

# Simplifying constant for the plug and chug
k = (electrical_conductivity * pole_disk_distance ** 2 * pole_area * disk_thickness) * B**2

def best_fit(x,m,c,d):
    return c-d*(np.exp(m*x))
#Plotting results. When I print popt for each line of best fit, it is to see if m is a constant or if this fit
#is wrong, basically.
for i in range(len(xdata)-1):
    plt.plot(xdata[i],ydata[i],'o',label=("R"+str(i+1)))
    popt, pcov = curve_fit(best_fit, xdata[i], ydata[i])
    plt.plot(xdata[i], best_fit(xdata[i], *popt), '-')
    print(popt)
plt.plot(xdata[12],ydata[12],'o',label=("R13"))
popt,pcov=curve_fit(best_fit,xdata[12],ydata[12])
plt.plot(xdata[12],best_fit(xdata[12],*popt),'-')
print(popt)

plt.ylim(0)
plt.xlim(0)
plt.legend()
plt. show()
