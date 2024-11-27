import tkinter as tk







# Function for button click (placeholder for now)
def load_audio():
  # Add your audio file
  print("Loading audio...")  #Switch this out for the name of the file










####################################################################################
# Create the main window
window = tk.Tk()
window.title("SPIDAM V13 Audio Loader")

# Set the window size
window.geometry("300x200")

# Create a label
label = tk.Label(window, text="Hello, world!")
label.pack()

# Create a button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

# Start the event loop
window.mainloop()