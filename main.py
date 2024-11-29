import tkinter as tk
from tkinter import filedialog, ttk
from pydub import AudioSegment

def load_audio():
    # Open a file dialog to select an audio file
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.*"), ("All Files", "*.mp3 *.wav *.ogg"))
    )
    if file_path:
        file_name_var.set(file_path)  # Set the file name in the variable
    # Replace with your audio loading logic
    if file_name_var.get():
        print(f"Loading audio: {file_name_var.get()}")  # Placeholder message
        notification_var.set(f"Loading audio: {file_name_var.get()}")
        clear_notification()

        # Automatically call convert_to_wav_and_get_duration
        convert_to_wav_and_get_duration()

    else:
        notification_var.set("No file selected!")
        clear_notification()


def convert_to_wav_and_get_duration():
    # Check if a file is selected
    if file_name_var.get():
        try:
            # Load the selected audio file
            audio = AudioSegment.from_file(file_name_var.get())

            # Modify output path to match original file with .wav extension
            original_path = file_name_var.get()
            # Replace backslashes with forward slashes if needed
            original_path = original_path.replace("\\", "/")  # For Windows compatibility
            output_path = f"{original_path[:-4]}.wav"  # Change extension to .wav

            # Convert to .wav and save
            audio.export(output_path, format="wav")

            # Get the duration in seconds
            duration_seconds = len(audio) / 1000  # Audio length in milliseconds

            # Display the duration in the notification bar
            notification_var.set(f"Converted to .wav. Duration: {duration_seconds:.2f} seconds")

            # Display the duration in the Audio Duration frame
            duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")

        except Exception as e:
            notification_var.set(f"Error processing file: {e}")
    else:
        notification_var.set("No file selected!")
    clear_notification()

def clear_notification():
    #Clear the notification bar after a short delay
    #window.after(10000, lambda: notification_var.set(""))  # 10 seconds delay
    print("Hello")


######################################################################################

# Create the main window
window = tk.Tk()
window.title("Audio Converter")

# Set the window size
window.geometry("500x400")

# Create a StringVar for the notification text
notification_var = tk.StringVar()

# Create a StringVar to hold the selected file name
file_name_var = tk.StringVar()

# Create the notification bar
notification_bar = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create a label for the notification text
notification_text = tk.Label(notification_bar, textvariable=notification_var)
notification_text.pack(side=tk.LEFT)

# Create a "Load Audio" button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

# Create a LabelFrame to display duration
duration_frame = ttk.LabelFrame(window, text="Audio Duration")
duration_frame.pack()

# Create a label to display the duration
duration_label = ttk.Label(duration_frame, text="")
duration_label.pack()

# Update the duration label
#duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")

# Create a label to display the selected file name
file_name_label = tk.Label(window, textvariable=file_name_var, wraplength=400, anchor="w", justify="left")
file_name_label.pack()  # Position the label

# Start the event loop
window.mainloop()