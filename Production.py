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
    ydata[i] = (2*np.pi*(ydata[i]))/16/60
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

for i in range(len(xdata)-1):
    plt.plot(xdata[i],ydata[i],label=("R"+str(i+1)))
plt.plot(xdata[12],ydata[12],label=("R13"))

plt.ylim(0)
plt.xlim(0)
plt.legend()
plt. show()
