import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

Location = "C:/Users/cuco2/Desktop/Physics/Year 2/Experimental physics/Semester 2/PR48_data1.xlsx"
sheet_2 = pd.read_excel(Location, sheet_name = "I = 0.098")

xdata1 = sheet_2["T1(s)"]
xdata1 = xdata1.dropna()
ydata1 = sheet_2["R1"]*0.10472/16
ydata1 = ydata1.dropna()

xdata2 = sheet_2["T2(s)"]
xdata2 = xdata2.dropna()
ydata2 = sheet_2["R2"]/16*0.10472
ydata2 = ydata2.dropna()

xdata3 = sheet_2["T3(s)"]
xdata3 = xdata3.dropna()
ydata3 = sheet_2["R3"]/16*0.10472
ydata3 = ydata3.dropna()

xdata4 = sheet_2["T4(s)"]
xdata4 = xdata4.dropna()
ydata4 = sheet_2["R4"]/16*0.10472
ydata4 = ydata4.dropna()

xdata5 = sheet_2["T5(s)"]
xdata5 = xdata5.dropna()
ydata5 = sheet_2["R5"]/16*0.10472
ydata5 = ydata5.dropna()

xdata6 = sheet_2["T6(s)"]
xdata6 = xdata6.dropna()
ydata6 = sheet_2["R6"]/16*0.10472
ydata6 = ydata6.dropna()

xdata = pd.Series(dtype = float)
xdata = xdata.append(xdata1, ignore_index = True)
xdata = xdata.append(xdata2, ignore_index = True)
xdata = xdata.append(xdata3, ignore_index = True)
xdata = xdata.append(xdata4, ignore_index = True)
xdata = xdata.append(xdata5, ignore_index = True)
xdata = xdata.append(xdata6, ignore_index = True)

ydata = pd.Series(dtype = float)
ydata = ydata.append(ydata1, ignore_index = True)
ydata = ydata.append(ydata2, ignore_index = True)
ydata = ydata.append(ydata3, ignore_index = True)
ydata = ydata.append(ydata4, ignore_index = True)
ydata = ydata.append(ydata5, ignore_index = True)
ydata = ydata.append(ydata6, ignore_index = True)

def best_fit(t,a,b,c):
    return a*np.exp(-1*b*t)+c

popt, pcov = curve_fit(best_fit, xdata, ydata, maxfev = 10000)
time = np.linspace(0,20,200)
plt.scatter(xdata, ydata)
plt.plot(time, best_fit(time, *popt), label = "fit")
plt.show()
print(popt)