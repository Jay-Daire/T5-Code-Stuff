import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataframe = pd.read_csv("C:/Users/cuco2/Desktop/Physics/Year 2/Experimental physics/Semester 2/Computing coursework/Python code/CSV files lab/al02.csv")

time = dataframe["second"]
voltage = dataframe["Volt"]

def get_rid_of_t_smaller_than_0(time, voltage):
    for i in range(len(time)):
        if time[i] == 0:
            index = i
    corrected_time = time[index: ]
    corrected_time = corrected_time.reset_index()
    corrected_time = corrected_time["second"]
    corrected_voltage = voltage[index: ]
    corrected_voltage = corrected_voltage.reset_index()
    corrected_voltage = corrected_voltage["Volt"]
    return corrected_time, corrected_voltage

def period_finder(time, voltage, number_of_strips = 1):
    times = []
    periods = []
    v_ang = []
    for i in range(len(voltage)):
        if voltage[i] < 10:
            times.append(time[i])
    for i in range(len(times)-1):
        t1 = time[i]
        t2 = times[i+1]
        periods.append(t2-t1)
    for i in periods:
        v_ang.append(2*np.pi/(i*number_of_strips))
    return v_ang, times

new_time, new_voltage = get_rid_of_t_smaller_than_0(time, voltage)
list_of_periods, new_new_times = period_finder(new_time, new_voltage)
plt.plot(new_new_times[:-1], list_of_periods)
plt.show()