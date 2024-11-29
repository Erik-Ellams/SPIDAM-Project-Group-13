import tkinter as tk
from tkinter import filedialog, ttk
from pydub import AudioSegment
import tempfile
import os
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave


def load_audio():
    """
    Opens a file dialog to select an audio file and starts the processing chain.
    """
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.*"), ("All Files", "*.mp3 *.wav *.ogg"))
    )
    if file_path:
        file_name_var.set(file_path)  # Set the file name in the variable
        notification_var.set(f"Loading audio: {file_path}")

        # Start the processing chain
        output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        convert_to_wav(file_path, output_path)
    else:
        notification_var.set("No file selected!")


def convert_to_wav(file_path, output_path):
    """
    Converts the audio file at 'file_path' to WAV format and saves it to 'output_path'.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        audio.export(output_path, format="wav")
        notification_var.set("Converted to WAV format.")

        # Proceed to remove metadata
        metadata_free_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        remove_metadata(output_path, metadata_free_path)
    except Exception as e:
        notification_var.set(f"Error in conversion: {e}")


def remove_metadata(source_file, destination_file):
    """
    Removes metadata from the 'source_file' and saves the result to 'destination_file'.
    """
    try:
        # Remove existing temporary file, if any
        if os.path.exists(destination_file):
            os.remove(destination_file)

        subprocess.run(["ffmpeg", "-y", "-i", source_file, "-map_metadata", "-1", destination_file], check=True)
        notification_var.set("Metadata removed.")

        # Proceed to get duration
        get_duration(destination_file)

        # Display the waveform
        display_waveform(destination_file)

    except Exception as e:
        notification_var.set(f"Error in removing metadata: {e}")


def get_duration(file_path):
    """
    Gets the duration of the provided audio file (assuming it's already converted to WAV).
    """
    try:
        # Get the duration using pydub
        audio = AudioSegment.from_file(file_path)
        duration_seconds = len(audio) / 1000  # Audio length in milliseconds

        # Display the duration in the notification bar
        notification_var.set(f"Duration: {duration_seconds:.2f} seconds")
        duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")
    except Exception as e:
        notification_var.set(f"Error getting duration: {e}")

def display_waveform(file_path):
    """
    Displays the waveform of the .wav file in the GUI.
    """
    try:
        # Read the WAV file
        with wave.open(file_path, "r") as wav_file:
            n_frames = wav_file.getnframes()
            n_channels = wav_file.getnchannels()
            framerate = wav_file.getframerate()
            audio_data = wav_file.readframes(n_frames)

        # Convert audio data to numpy array
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)

        # If the audio has multiple channels, take the first one
        if n_channels > 1:
            audio_samples = audio_samples[::n_channels]

        # Create the waveform plot
        fig, ax = plt.subplots(figsize=(5, 2))
        time_axis = np.linspace(0, len(audio_samples) / framerate, num=len(audio_samples))
        ax.plot(time_axis, audio_samples, color="blue")
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        # Clear existing widgets in the frame
        for widget in waveform_frame.winfo_children():
            widget.destroy()

        # Embed the plot in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=waveform_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        notification_var.set("Waveform displayed.")
    except Exception as e:
        notification_var.set(f"Error displaying waveform: {e}")


######################################################################################

# Create the main window
window = tk.Tk()
window.title("Audio Converter")

# Set the window size
window.geometry("600x500")

# Create a StringVar for the notification text
notification_var = tk.StringVar()

# Create a StringVar to hold the selected file name
file_name_var = tk.StringVar()

# Create the notification bar
notification_bar = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create a frame for the notification area
notification_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Add a label above the notification frame for the title
notification_title = tk.Label(window, text="Notification Bar", font=("Arial", 10, "bold"))
notification_title.pack(side=tk.BOTTOM)

# Add a label inside the notification frame to display the text
notification_text = tk.Label(notification_frame, textvariable=notification_var)
notification_text.pack(side=tk.LEFT, padx=5, pady=5)

# Create a "Load Audio" button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.pack()  # Position the button

# Create a LabelFrame to display duration
duration_frame = ttk.LabelFrame(window, text="Audio Duration")
duration_frame.pack()

# Create a label to display the duration
duration_label = ttk.Label(duration_frame, text="")
duration_label.pack()

# Create a label to display the selected file name
file_name_label = tk.Label(window, textvariable=file_name_var, wraplength=400, anchor="w", justify="left")
file_name_label.pack()  # Position the label

# Create a frame for the waveform display
waveform_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
waveform_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Start the event loop
window.mainloop()