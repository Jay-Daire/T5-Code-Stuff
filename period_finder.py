import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Apparently not every measurement starts at t = 0, to get good plots we
# need to look at the plots of the data and estimate
# when it starts declining. Means we will need to briefly glance at around
# 2k plots


#RUN CODE FROM TERMINAL DO NOT EDIT

def get_rid_of_useless_times(time, voltage, time_when_decay_starts):
    for i in range(len(time)):
        if np.floor(time[i]) == time_when_decay_starts:
            index = i
    corrected_time = time[index: ]
    corrected_time = corrected_time.reset_index()
    corrected_time = corrected_time["second"]
    corrected_voltage = voltage[index: ]
    corrected_voltage = corrected_voltage.reset_index()
    corrected_voltage = corrected_voltage["Volt"]
    return corrected_time, corrected_voltage

def period_finder(time, voltage, number_of_strips = 1):
    # Allocate memory for all the series, the values are placeholders but
    # should be big enough for all the files
    times = pd.Series(dtype = float, index = (i for i in range(30000)))
    periods = pd.Series(dtype = float,index = (i for i in range(10000)))
    v_ang = pd.Series(dtype= float, index = (i for i in range(10000)))
    # loop counter
    j = 0
    for i in range(len(voltage)):
        if voltage[i] < 10:
            times[j] = time[i]
            j= j+1
    # Reset j to reuse it
    j = 0
    # Drop all the values in the times series that have no values stored
    times = times.dropna()
    for i in range(len(times)-1):
        t1 = time[i]
        t2 = times[i+1]
        periods[j] = t2-t1
        j = j+1
    # Reset j to reuse it
    j = 0
    # Drop all the values in the times series that habe no values stored
    periods = periods.dropna()
    for i in periods:
        v_ang[j] = 2*np.pi/(i*number_of_strips)
        j= j+1
    # Drop all the values in the angular velocities series that have no values stored
    v_ang = v_ang.dropna()
    return v_ang, times

def plot_a_file():
    #Plots a single file from a dataset
    name_of_file = input("What is the name of the file you want analyzed? ")
    dataframe = pd.read_csv(
        f"C:/Users/cuco2/Desktop/Physics/Year 2/Experimental physics/Semester 2/Computing coursework/Python code/CSV files lab/{name_of_file}.csv")
    measurement_start = int(input("To the nearest integer, when would you say decay starts for this measurement? "))
    time = dataframe["second"]
    voltage = dataframe["Volt"]
    new_time, new_voltage = get_rid_of_useless_times(time, voltage, measurement_start)
    angular_velocity, time_axis = period_finder(new_time - measurement_start, new_voltage)
    plt.plot(time_axis[:-1], angular_velocity)
    answer = input("Do you want the title displayed in the image? y/n")
    if answer == "yes" or answer == "y":
        plt.title(f"{name_of_file}")
        plt.xlabel("time (s)")
        plt.ylabel("$\omega\ \mathrm{rad/s}$")
        plt.xlim(0, )
        plt.savefig(f"{name_of_file}plot")
    else:
        plt.xlabel("time (s)")
        plt.ylabel("$\omega\ (\mathrm{rad/s})$")
        plt.xlim(0, )
        plt.savefig(f"{name_of_file}plot")
    return None

def overplot(number_of_plots):
    #Plots several files in the same graph
    name_of_plot = input("What will you call your plot? ")
    for i in range(number_of_plots):
        # save something to a df, then plot that dataframe and save the figure otuside the for loop
        name_of_file = input(f"What's the name of the file no. {i} you want to plot")
        dataframe = pd.read_csv(
            f"C:/Users/cuco2/Desktop/Physics/Year 2/Experimental physics/Semester 2/Computing coursework/Python code/CSV files lab/{name_of_file}.csv")
        time = dataframe["second"]
        voltage = dataframe["Volt"]
        measurement_start = int(
            input("To the nearest integer, when would you say decay starts for this measurement? "))
        new_time, new_voltage = get_rid_of_useless_times(time, voltage, measurement_start)
        angular_velocity, time_axis = period_finder(new_time - measurement_start, new_voltage)
        plt.plot(time_axis[:-1], angular_velocity)
        plt.legend(f"{name_of_file}")
    plt.savefig(f"{name_of_plot}")

if __name__ == "main":

    Guten_morgen = input("Do you want to overplot several measurements? If so, how many?")

    try:
        Guten_morgen = int(Guten_morgen)
        if Guten_morgen <= 0:
            plot_a_file()
        if Guten_morgen == 1:
            print("Then you don't want to overplot anything, dumbass")
            plot_a_file()
        else: #They do want to overplot several measuerements
            overplot(Guten_morgen)
    except ValueError:  #the user does not want to analyze more than one file
        plot_a_file()