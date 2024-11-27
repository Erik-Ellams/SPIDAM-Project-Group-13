import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([0, 6])
ypoints = np.array([0, 250])

plt.plot(xpoints, ypoints)
plt.show()

# Create the main window
window = tk.Tk()
window.title("My First GUI")

# Set the window size
window.geometry("300x200")

# Create a label
label = tk.Label(window, text="Hello, world!")
label.pack()

# Start the event loop
window.mainloop()

