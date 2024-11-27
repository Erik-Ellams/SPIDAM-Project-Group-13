import tkinter as tk

def load_audio():
    # Replace with your audio loading logic (using libraries like playsound or pygame)
    print("Loading audio...")  # Placeholder message

    # Update the notification bar
    notification_var.set("Audio loading...")

def clear_notification():
    # Clear the notification bar after a short delay
    window.after(2000, notification_var.set(""))  # 2 seconds delay

def create_notification_bar():
    # Create a frame for the notification bar
    notification_bar = tk.Frame(window, relief=tk.SUNKEN, bd=1)
    notification_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Create a label for the notification text
    notification_text = tk.Label(notification_bar, textvariable=notification_var)
    notification_text.pack(side=tk.LEFT)



######################################################################################

# Create the main window
window = tk.Tk()
window.title("SPIDAM V13 Audio Loader")

# Set the window size
window.geometry("500x400")

# Create a StringVar for the notification text
notification_var = tk.StringVar()

# Call the function to create the notification bar
create_notification_bar()

# Create a button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

# Start the event loop
window.mainloop()