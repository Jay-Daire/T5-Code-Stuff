import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

data=pd.read_excel(r"C:\Users\jonat\OneDrive\Documents\University\Year 2 Semester 2\PR48_data1.xlsx",sheet_name="B")
xdata=data["CoilCurrent"]
ydata=data["MagneticFieldStrength"]



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

plt.plot(xdata,ydata)

plt.ylim(0)
plt.xlim(0)
plt.legend()
plt. show()
