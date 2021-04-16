import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import ExponentialModel, ConstantModel

# Apparently not every measurement starts at t = 0, to get good plots we
# need to look at the plots of the data and estimate
# when it starts declining. Means we will need to briefly glance at around
# 2k plots

editor = input("Who's editing?")
if editor == "J" or editor == "Jonathan" or editor == "j":
    path = "C:/Users/jonat/Documents/University/Year 2 Semester 2/NewData/High speed/Steel/0.047/"
    skip = 1
else:
    path = "C:/Users/cuco2/Desktop/Physics/Year 2/Experimental physics/Semester 2/Computing coursework/Python code/CSV files lab/"
    skip = 0


# RUN CODE FROM TERMINAL DO NOT EDIT

def colourmatch():
    for item in ['r','g','b','c','m','y','k']:
        yield item
colour=colourmatch()

def time_trimmer(time, voltage, decay_start):
    if decay_start == 0:
        for i in range(len(time)):
            if time[i] == 0:
                index = i
    else:
        for i in range(len(time)):
            if np.floor(time[i]) == decay_start:
                index = i

    # Correcting the time so that it starts to count when the meas starts
    corrected_time = time[index:]  # Creating a new array that goes from index (the point where the meas starts) to
    # the end of the array
    corrected_time = corrected_time.reset_index()  # Resetting the index so that the series starts at 0
    corrected_time = corrected_time["second"]  # Renaming the new series
    # Saving the first value of the new, corrected series so that it does not change in the loop
    first_value = corrected_time[0]
    # Subtracting the first value in our corrected value to each value in the array to displace
    # everything to the left and make the plot start plotting at 0
    for i in range(len(corrected_time)):
        corrected_time[i] = corrected_time[i] - first_value

    # Correcting the voltage so that it starts when the meas starts
    corrected_voltage = voltage[index:]  # Creating a new array that goes from index (the point where the meas starts)
    # to the end of the array
    corrected_voltage = corrected_voltage.reset_index()  # Resetting the index so that the series starts at 0
    corrected_voltage = corrected_voltage["Volt"]  # Renaming the new series

    # Returns the corrected series
    return corrected_time, corrected_voltage


def period_finder(time, voltage, strip_no=1):
    # Allocate memory for all the series, the values are placeholders but
    # should be big enough for all the files
    strip_passing_oscilloscope = pd.Series(dtype=float, index=(i for i in range(30000)))
    periods = pd.Series(dtype=float, index=(i for i in range(10000)))
    v_ang = pd.Series(dtype=float, index=(i for i in range(10000)))
    corrected_time_values = pd.Series(dtype=float, index = (i for i in range(10000)))
    # loop counter
    j = 0
    for i in range(len(voltage)):  # Counts every voltage drop, which corresponds to the strip passing the oscilloscope
        if voltage[i] < 10:
            strip_passing_oscilloscope[j] = time[i]
            j = j + 1  # Increase the value of j so that the next value is placed in the next position in the array
    # Reset j to reuse it
    j = 0
    # Drop all the values in the strip_passing_oscilloscope series that have no values stored
    strip_passing_oscilloscope = strip_passing_oscilloscope.dropna()

    for i in range(len(strip_passing_oscilloscope) - 1):  # Finding the period of a revolution
        t1 = time[i]  # One value in the array
        t2 = strip_passing_oscilloscope[i + 1]  # Next value in the array
        periods[j] = t2 - t1  # The period is the difference between two consecutive times, since there's only 1 strip
        j = j + 1  # Increase the value of j so that the next value is placed in the next position in the array

    # Reset j to reuse it
    j = 0

    # Drop all the values in the times series that have no values stored
    periods = periods.dropna()

    for i in periods:  # Finding the angular velocities
        v_ang[j] = 2 * np.pi / (i * strip_no)  # w = 2 * PI / T, where T is the period
        j = j + 1

    # Drop all the values in the angular velocities series that have no values stored
    v_ang = v_ang.dropna()
    for i in range(len(strip_passing_oscilloscope)):
        # strip_passing_oscilloscope[i] = strip_passing_oscilloscope[i] - strip_passing_oscilloscope[0]
        temp_value = strip_passing_oscilloscope[i] - strip_passing_oscilloscope[0]
        strip_passing_oscilloscope [i] = strip_passing_oscilloscope[i] - strip_passing_oscilloscope[0]
        corrected_time_values[i] = temp_value
    return v_ang, strip_passing_oscilloscope


# Model data as exponential + constant
exp_mod = ExponentialModel(prefix = "exp_")
const_mod = ConstantModel(prefix = "const_")


Model = exp_mod + const_mod

params = Model.make_params()


def plot_a_file():
    # Plots a single file from a dataset
    name_of_file = input("What is the name of the file you want analyzed? ")

    # Assign a dataframe to the data stored in the file (essentially a 2D array)
    dataframe = pd.read_csv(
        f"{path}{name_of_file}.csv", skiprows=skip)

    # Asking the user to estimate when the measurement starts
    measurement_start = int(input("To the nearest integer, when would you say decay starts for this measurement? "))

    # Assigning series to the values in the dataframe
    time = dataframe["second"]
    voltage = dataframe["Volt"]

    # Creating arrays of corrected times and corrected voltages with the time_trimmer function
    new_time, new_voltage = time_trimmer(time, voltage, measurement_start)

    # Finding the period and correcting for the time if the measurement stars at t != 0
    angular_velocity, time_axis = period_finder(new_time, new_voltage)

    # Setting the colors of the plot
    acolour = next(colour)

    # Plotting the functions
    plt.plot(time_axis[:-1], angular_velocity, marker = 'x', markersize = 4, color = "k", linestyle = "none")

    # Fitting a line of best fit
    out = Model.fit(angular_velocity, params, x = time_axis)
    # Plotting the line of best fit
    plt.plot(time_axis[:-1], out.best_fit, color = "k", linestyle = "-")
    # Printing the values for the best fit function
    file = open(f"{name_of_file}.txt", "w")
    file.write(out.fit_report())
    file.close()
    plt.legend()
    # Old print function, use if new one is wrong or doesn't work


    # Title displayed - Do we want it?
    answer = input("Do you want the title displayed in the image? y/n")

    # Yes
    if answer == "yes" or answer == "y":
        plt.title(f"{name_of_file}")

    plt.xlabel("time (s)")
    plt.ylabel("$\omega\ \mathrm{rad/s}$")
    plt.xlim(0, )
    plt.savefig(f"{name_of_file}plot")
    plt.close()


    # Kinda redundant, I don't think a function in Python has to return anything
    return None


def overplot(number_of_plots):
    # Plots several graphs in the same question

    # Assigning the name of the plot
    name_of_plot = input("What will you call your plot? ")
    file = open(f"{name_of_plot}.txt", "a")
    for i in range(number_of_plots):  # Plotting the different plots

        # Getting the name of the file that we want to plot
        name_of_file = input(f"What's the name of the file no. {i} you want to plot")

        # Putting the file into a dataframe
        dataframe = pd.read_csv(
            f"{path}{name_of_file}.csv", skiprows=skip)

        # Creating a series with the time values and the voltage values:
        time = dataframe["second"]
        voltage = dataframe["Volt"]

        # Approximating the initial value of t when the measurement starts
        measurement_start = int(
            input("To the nearest integer, when would you say decay starts for this measurement? "))

        # Assigning corrected times and voltages to a series.
        new_time, new_voltage = time_trimmer(time, voltage, measurement_start)

        # Finding the angular velocities and time values, accounting for the case when t != 0
        angular_velocity, time_axis = period_finder(new_time, new_voltage)

        # Setting a color for the plot

        acolour = next(colour)

        # Plotting the file, and labeling it with the name of the meas we're plotting
        plt.plot(time_axis[:-1], angular_velocity, 'x', label=f"{name_of_file}", markersize = 4, color = acolour, linestyle = "none")

        # Doing the best fit
        out = Model.fit(angular_velocity, params, x=time_axis)
        # Plotting the line of best fit
        plt.plot(time_axis[:-1], out.best_fit, color = acolour, label = "best fit")

        # Printing the values for the best fit function
        file.write(f"\nReport for file {name_of_file}")
        file.write(out.fit_report())

        # Old print function, use if new one is wrong or doesn't work
        # print("The values for ", name_of_plot, " are: ", popt)

    file.close()
    # The plot should start with t = 0
    plt.xlim(0, )
    legend =  input("Do you want the legend to be shown? y/n")
    if legend == "yes" or legend == "y":
        plt.legend()
    # Saving the plot with the name indicated by the user
    plt.savefig(f"{name_of_plot}")

    # Closing the plot so that we don't get 10000 overlapped files as we rerun the progra,
    plt.close()


if __name__ == "__main__":
    Guten_morgen = input("Do you want to overplot several measurements? If so, how many?")

    try:
        Guten_morgen = int(Guten_morgen)
        if Guten_morgen <= 0:
            plot_a_file()
        if Guten_morgen == 1:
            print("Then you don't want to overplot anything, dumbass")
            plot_a_file()
        else:  # They do want to overplot several measuerements
            overplot(Guten_morgen)
    except ValueError:  # the user does not want to analyze more than one file
        plot_a_file()
