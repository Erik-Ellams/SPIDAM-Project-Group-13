import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

time = np.array([0, 6])
frequency = np.array([0, 250])



# Function for button click (placeholder for now)
def load_audio():
  # Add your audio file
  print("Loading audio...")  #Switch this out for the name of the file

#Function to show low frequency graph
def show_low_frequency():
    plt.plot(frequency, time)
    plt.show()

####################################################################################
# Create the main window
window = tk.Tk()
window.title("My First GUI")

# Set the window size
window.geometry("300x200")

# Create a label
label = tk.Label(window, text="Hello, world!")
label.pack()

# Create a button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

load_freq_button = tk.Button(window, text="Plot Low Frequency", command=show_low_frequency)
load_freq_button.pack()

# Start the event loop
window.mainloop()
