import tkinter as tk

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