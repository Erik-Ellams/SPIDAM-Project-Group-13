import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from tkinter import filedialog
import subprocess
import os

class plot:
    def __init__(self, file_name):
        self.file_name = file_name
    def display(self):
        try:
            sample_rate, data = wavfile.read(self.file_name)

            #plt.plot(self.frequency, self.time, self.file_name)

            #ffmpeg - i input_file - ar 44100 - ac 1 output.wav

            if len(data.shape) > 1:
                data = data[:, 0]

            plt.figure(figsize=(10, 6))
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            cbar = plt.colorbar(im)
            cbar.set_label('Intensity (dB)')

            plt.title("Spectrogram")
            plt.xlabel("Time [s]")
            plt.ylabel("Frequency [Hz]")
            plt.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            notification_var.set("Error displaying plot. Check the file format.")
            clear_notification()

audio_name = "none"

def is_valid_wav(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(4)
        return header in [b'RIFF', b'RIFX', b'RF64']

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        notification_var.set("FFmpeg is not installed. Please install it and try again.")
        return False

def load_audio():
    global audio_name
    # Open a file dialog to select an audio file
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*"))
    )

    if file_path:
        original_format = os.path.splitext(file_path)[1].lower()
        if original_format != ".wav":
            # Convert to WAV format
            converted_file = os.path.splitext(file_path)[0] + "_converted.wav"
            notification_var.set(f"Converting {os.path.basename(file_path)} to WAV...")
            audio_name = convert_to_wav(file_path, converted_file)
            if audio_name:
                notification_var.set(f"Converted and loaded: {os.path.basename(audio_name)}")
                file_name_var.set(audio_name)
            else:
                notification_var.set("Conversion failed!")
                audio_name = "none"
                return
        else:
            if is_valid_wav(file_path):
                file_name_var.set(file_path)
                audio_name = file_name_var.get()
                notification_var.set(f"Loaded: {os.path.basename(file_name_var.get())}")
            else:
                notification_var.set("Invalid WAV file selected!")
                audio_name = "none"
    # Replace with your audio loading logic
    if file_name_var.get():
        print(f"Loading audio: {file_name_var.get()}")  # Placeholder message
        audio_name = file_name_var.get()
        notification_var.set(f"Loading audio: {file_name_var.get()}")
        clear_notification()
    else:
        is_valid_wav(file_path)
        notification_var.set("No file selected!")
        clear_notification()

def clear_notification():
    # Clear the notification bar after a short delay
    window.after(2000, lambda: notification_var.set(""))  # 2 seconds delay

def convert_to_wav(input_file, output_file):
    """
    Converts an audio file to WAV format using FFmpeg.
    """

    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', input_file, '-ar', '44100', '-ac', '1', output_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if os.path.exists(output_file):
            return output_file
        else:
            print("Conversion failed: Output file not created.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr.decode()}")
        return None


def plot_low_frequency():
    if audio_name and os.path.exists(audio_name):
        notification_var.set("Processing spectrogram...")
        window.update_idletasks()  # Update UI before processing
        low = plot(audio_name)
        low.display()
        notification_var.set("Spectrogram displayed.")
    else:
        notification_var.set("No valid audio file loaded!")

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

#Create plot button
plot_button = tk.Button(window, text="Plot Low Frequency", command=plot_low_frequency)
plot_button.pack()

# Start the event loop
window.mainloop()