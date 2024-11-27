import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

time_low = np.array([0, 6])
frequency_low = np.array([0, 250])

time_med = np.array([0, 6])
frequency_med = np.array([0, 250])

time_high = np.array([0, 6])
frequency_high = np.array([0, 250])

class plot:
    def __init__(self, time, frequency):
        self.time = time
        self.frequency = frequency
    def display(self):
        plt.plot(frequency_low, time_low)
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.show()
        plt.show()

low = plot(time_low, frequency_low)
med = plot(time_med, frequency_med)
high = plot(time_high, frequency_high)

low.display()