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
import scipy.fftpack


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

        # Calculate and display the dominant frequency
        Frequency_Calculation(destination_file)

        # Calculate and display the RT60 Low
        RT60LOW_Calculation(destination_file)

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

def Frequency_Calculation(file_path):
    """
    Calculates the dominant frequency of the .wav file and updates the frequency_label.
    """
    try:
        # Read the WAV file
        with wave.open(file_path, "r") as wav_file:
            n_frames = wav_file.getnframes()
            framerate = wav_file.getframerate()
            n_channels = wav_file.getnchannels()
            audio_data = wav_file.readframes(n_frames)

        # Convert audio data to a numpy array
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)

        # If the audio has multiple channels, use only the first channel
        if n_channels > 1:
            audio_samples = audio_samples[::n_channels]

        # Perform FFT and find frequencies
        fft_result = np.abs(scipy.fftpack.fft(audio_samples))
        frequencies = np.fft.fftfreq(len(fft_result), d=1 / framerate)

        # Consider only positive frequencies
        positive_freqs = frequencies[:len(frequencies) // 2]
        positive_fft_result = fft_result[:len(fft_result) // 2]

        # Find the dominant frequency
        dominant_frequency = positive_freqs[np.argmax(positive_fft_result)]

        # Update the frequency label in the GUI
        frequency_label.config(text=f"Frequency: {dominant_frequency:.2f} Hz")
        notification_var.set(f"Calculated Frequency: {dominant_frequency:.2f} Hz")

    except Exception as e:
        notification_var.set(f"Error in frequency calculation: {e}")

def RT60LOW_Calculation(file_path):
    """
    Calculates the RT60 Low value of the .wav file and updates the rt60_low_label.
    """
    try:
        # Load the audio file
        with wave.open(file_path, "r") as wav_file:
            n_frames = wav_file.getnframes()
            framerate = wav_file.getframerate()
            n_channels = wav_file.getnchannels()
            audio_data = wav_file.readframes(n_frames)

        # Convert audio data to numpy array
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)

        # If the audio has multiple channels, use only the first channel
        if n_channels > 1:
            audio_samples = audio_samples[::n_channels]

        # Simulated RT60 Low calculation (using simple decay analysis for demonstration)
        # Assume low frequencies are the first 20% of the FFT spectrum
        fft_result = np.abs(scipy.fftpack.fft(audio_samples))
        low_freq_fft = fft_result[:len(fft_result) // 5]  # First 20% frequencies

        # Estimate decay time (this is a placeholder; real RT60 would use a more complex model)
        rt60_low_value = np.mean(low_freq_fft) / max(low_freq_fft) * 1000  # Placeholder scaling

        # Update the label in the GUI
        rt60_low_label.config(text=f"RT60 Low: {rt60_low_value:.2f} ms")
        notification_var.set(f"RT60 Low Calculated: {rt60_low_value:.2f} ms")

    except Exception as e:
        notification_var.set(f"Error in RT60 Low calculation: {e}")

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

        # Create the waveform plot with a larger figure size
        fig, ax = plt.subplots(figsize=(12, 6))  # Adjusted figure size
        time_axis = np.linspace(0, len(audio_samples) / framerate, num=len(audio_samples))
        ax.plot(time_axis, audio_samples, color="blue")
        ax.set_title("Waveform", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Amplitude (dB)", fontsize=12)
        ax.grid(True)  # Optional: Add a grid for better readability

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
window.title("SPIDAM V13 Audio Loader")

# Set the window size
window.geometry("1200x1000")

# Create a StringVar for the notification text
notification_var = tk.StringVar()

# Create a StringVar to hold the selected file name
file_name_var = tk.StringVar()

# Create a LabelFrame for the file name
file_name_frame = ttk.LabelFrame(window, text="File Name")
file_name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Add a label inside the frame to display the file name
file_name_label = tk.Label(file_name_frame, textvariable=file_name_var, wraplength=400, anchor="w", justify="left")
file_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Create the notification bar
notification_bar = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_bar.grid(row=1, column=0, sticky="ew")

# Create a frame for the notification area
notification_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_frame.grid(row=2, column=0, sticky="ew")

# Create a "Load Audio" button
load_button = tk.Button(window, text="Load Audio", command=load_audio)
load_button.grid(row=4, column=0, pady=10)

# Create a "Load RT60 Low" button
RT60LOW_button = tk.Button(window, text="Load RT60 Low", command=load_audio)
RT60LOW_button.grid(row=4, column=1, pady=10)

# Create a "Load RT60 Mid" button
RT60MID_button = tk.Button(window, text="Load RT60 MID", command=load_audio)
RT60MID_button.grid(row=4, column=2, pady=10)

# Create a "Load RT60 HIGH" button
RT60HIGH_button = tk.Button(window, text="Load RT60 HIGH", command=load_audio)
RT60HIGH_button.grid(row=4, column=3, pady=10)

# Create a LabelFrame to display duration
duration_frame = ttk.LabelFrame(window, text="Audio Duration")
duration_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

# Create a label to display the duration
duration_label = ttk.Label(duration_frame, text="")
duration_label.grid(row=0, column=0, padx=10, pady=5)

# Create a LabelFrame to display the Highest Resonance
frequency_frame = ttk.LabelFrame(window, text="Frequency")
frequency_frame.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

# Create a label to display the Highest Resonance
frequency_label = ttk.Label(frequency_frame, text="")
frequency_label.grid(row=0, column=0, padx=10, pady=5)

# Create a LabelFrame for RT60 Low (below Audio Duration and Frequency)
rt60_low_frame = ttk.LabelFrame(window, text="RT60 Low")
rt60_low_frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

# Add a label to the RT60 Low frame
rt60_low_label = ttk.Label(rt60_low_frame, text="")
rt60_low_label.grid(row=0, column=0, padx=10, pady=5)

# Create a LabelFrame for RT60 Mid (below Audio Duration and Frequency)
rt60_mid_frame = ttk.LabelFrame(window, text="RT60 Mid")
rt60_mid_frame.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

# Add a label to the RT60 Mid frame
rt60_mid_label = ttk.Label(rt60_mid_frame, text="")
rt60_mid_label.grid(row=0, column=0, padx=10, pady=5)

# Create a LabelFrame for RT60 High (below Audio Duration and Frequency)
rt60_high_frame = ttk.LabelFrame(window, text="RT60 High")
rt60_high_frame.grid(row=6, column=2, padx=10, pady=10, sticky="ew")

# Add a label to the RT60 High frame
rt60_high_label = ttk.Label(rt60_high_frame, text="")
rt60_high_label.grid(row=0, column=0, padx=10, pady=5)

# Create a frame for the waveform display
waveform_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
waveform_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Add a label above the notification frame for the title (optional)
notification_title = tk.Label(window, text="Notification Bar", font=("Arial", 10, "bold"))
notification_title.grid(row=9, column=0, columnspan=4, sticky="ew")

# Add the notification frame at the bottom
notification_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
notification_frame.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

# Add a label inside the notification frame to display the text
notification_text = tk.Label(notification_frame, textvariable=notification_var)
notification_text.pack(side=tk.LEFT, padx=5, pady=5)

# Configure the main window grid
window.grid_rowconfigure(8, weight=1)  # Allow waveform_frame to expand vertically
window.grid_rowconfigure(9, weight=0)  # Ensure notification stays fixed at the bottom
window.grid_rowconfigure(10, weight=0)  # Ensure notification stays fixed at the bottom
window.grid_columnconfigure(0, weight=1)  # Allow elements in column 0 to expand horizontally
window.grid_columnconfigure(1, weight=1)  # Allow elements in column 1 to expand horizontally
window.grid_columnconfigure(2, weight=1)  # Allow elements in column 2 to expand horizontally
window.grid_columnconfigure(3, weight=1)  # Allow elements in column 3 to expand horizontally

# Explicitly set widths for LabelFrames to prevent them from expanding excessively
file_name_frame.config(width=400)
duration_frame.config(width=200)
frequency_frame.config(width=200)
rt60_low_frame.config(width=200)
rt60_mid_frame.config(width=200)
rt60_high_frame.config(width=200)

# Update the waveform_frame to expand within its grid cell
waveform_frame.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Start the event loop
window.mainloop()