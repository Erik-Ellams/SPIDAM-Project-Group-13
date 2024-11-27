import tkinter as tk
from tkinter import filedialog

def load_audio():
    # Open a file dialog to select an audio file
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*"))
    )
    if file_path:
        file_name_var.set(file_path)  # Set the file name in the variable
    # Replace with your audio loading logic
    if file_name_var.get():
        print(f"Loading audio: {file_name_var.get()}")  # Placeholder message
        notification_var.set(f"Loading audio: {file_name_var.get()}")
        clear_notification()
    else:
        notification_var.set("No file selected!")
        clear_notification()

def clear_notification():
    # Clear the notification bar after a short delay
    window.after(2000, lambda: notification_var.set(""))  # 2 seconds delay



######################################################################################

# Create the main window
window = tk.Tk()
window.title("SPIDAM V13 Audio Loader")

# Set the window size
window.geometry("500x400")

# Create a StringVar for the notification text
notification_var = tk.StringVar()

# Create a StringVar to hold the selected file name
file_name_var = tk.StringVar()

# Create the notification bar (directly in the main script)
notification_bar = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create a label for the notification text
notification_text = tk.Label(notification_bar, textvariable=notification_var)
notification_text.pack(side=tk.LEFT)

# Create a label to display the selected file name
file_name_label = tk.Label(window, textvariable=file_name_var, wraplength=400, anchor="w", justify="left")
file_name_label.pack()  # Position the label

# Create a "Load Audio" button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

# Start the event loop
window.mainloop()