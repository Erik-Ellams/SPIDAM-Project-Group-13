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


class audioLoader:
    def __init__(self, window):
        self.window = window
        self.window.title("SPIDAM V13 Audio Loader")
        self.window.geometry("1200x1000")

        # Set the window background color to purple
        self.window.config(bg="#B0C4DE")

        # Variables
        self.notification_var = tk.StringVar()
        self.file_name_var = tk.StringVar()

        # Initialize UI
        self._setup_ui()

    def _setup_ui(self):
        self._create_file_name_frame()
        self._create_buttons()
        self._create_result_frames()
        self._create_notification_bar()
        self._create_waveform_frame()

    def _create_file_name_frame(self):
        window = self.window
        # Create a LabelFrame for the file name
        file_name_frame = ttk.LabelFrame(window, text="File Name")
        file_name_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add a label inside the frame to display the file name
        file_name_label = tk.Label(file_name_frame, textvariable=self.file_name_var, wraplength=400, anchor="w", justify="left")
        file_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def _create_buttons(self):
        window = self.window
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)

        load_button = tk.Button(window, text="Load Audio", command=self.load_audio, width=50, height=5)
        load_button.grid(row=0, column=2, pady=10)

        # Create a "Display default Waveform Graph" button
        RT60HIGH_button = tk.Button(window, text="Load Waveform Plot", command=self.load_audio)
        RT60HIGH_button.grid(row=4, column=0, pady=10)

        # Create a "Load RT60 Low" button
        RT60LOW_button = tk.Button(window, text="Load RT60 Low Plot", command=lambda: self.display_rt60("low"))
        RT60LOW_button.grid(row=4, column=1, pady=10)

        # Create a "Load RT60 Mid" button
        RT60MID_button = tk.Button(window, text="Load RT60 MID Plot", command=lambda: self.display_rt60("medium"))
        RT60MID_button.grid(row=4, column=2, pady=10)

        # Create a "Load RT60 HIGH" button
        RT60HIGH_button = tk.Button(window, text="Load RT60 HIGH Plot", command=lambda: self.display_rt60("high"))
        RT60HIGH_button.grid(row=4, column=3, pady=10)

    def _create_result_frames(self):
        self.duration_label = self._create_result_frame("Audio Duration", 5, 0)
        self.frequency_label = self._create_result_frame("Frequency", 5, 1)
        self.rt60_low_label = self._create_result_frame("RT60 Low", 6, 0)
        self.rt60_low_label.config(width=20)

        self.rt60_mid_label = self._create_result_frame("RT60 Mid", 6, 1)
        self.rt60_mid_label.config(width=20)

        self.rt60_high_label = self._create_result_frame("RT60 High", 6, 2)
        self.rt60_high_label.config(width=20)

    def _create_result_frame(self, title, row, column):
        frame = ttk.LabelFrame(self.window, text=title)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

        label = ttk.Label(frame, text="")
        label.grid(row=0, column=0, padx=10, pady=5)

        return label

    def _create_notification_bar(self):
        notification_frame = tk.Frame(self.window, relief=tk.SUNKEN, bd=1)
        notification_frame.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        label = tk.Label(notification_frame, textvariable=self.notification_var)
        label.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_waveform_frame(self):
        self.waveform_frame = tk.Frame(self.window, relief=tk.SUNKEN, bd=1)
        self.waveform_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.window.grid_rowconfigure(8, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def load_audio(self):
        """
        Opens a file dialog to select an audio file and starts the processing chain.
        """
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(("Audio Files", "*.*"), ("All Files", "*.mp3 *.wav *.ogg"))
        )
        if file_path:
            self.file_name_var.set(file_path)  # Set the file name in the variable
            self.notification_var.set(f"Loading audio: {file_path}")

            # Start the processing chain
            output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            self.convert_to_wav(file_path, output_path)
        else:
            self.notification_var.set("No file selected!")

    def convert_to_wav(self, file_path, output_path):
        """
        Converts the audio file at 'file_path' to WAV format and saves it to 'output_path'.
        """
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export(output_path, format="wav")
            self.notification_var.set("Converted to WAV format.")

            # Proceed to remove metadata
            metadata_free_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            self.remove_metadata(output_path, metadata_free_path)
        except Exception as e:
            self.notification_var.set(f"Error in conversion: {e}")

    def remove_metadata(self, source_file, destination_file):
        """
        Removes metadata from the 'source_file' and saves the result to 'destination_file'.
        """
        try:
            # Remove existing temporary file, if any
            if os.path.exists(destination_file):
                os.remove(destination_file)

            subprocess.run(["ffmpeg", "-y", "-i", source_file, "-map_metadata", "-1", destination_file], check=True)
            self.notification_var.set("Metadata removed.")

            # Proceed to get duration
            self.get_duration(destination_file)

            # Display the waveform
            self.display_waveform(destination_file)

            # Calculate and display the dominant frequency
            self.Frequency_Calculation(destination_file)

            # Calculate and display the RT60 Low
            self.RT60LOW_Calculation(destination_file)

            # Calculate and display the RT60 Mid
            self.RT60MID_Calculation(destination_file)

            # Calculate and display the RT60 High
            self.RT60HIGH_Calculation(destination_file)

        except Exception as e:
            self.notification_var.set(f"Error in removing metadata: {e}")
    def get_duration(self, file_path):
        """
        Gets the duration of the provided audio file (assuming it's already converted to WAV).
        """
        try:
            # Get the duration using pydub
            audio = AudioSegment.from_file(file_path)
            duration_seconds = len(audio) / 1000  # Audio length in milliseconds

            # Display the duration in the notification bar
            self.notification_var.set(f"Duration: {duration_seconds:.2f} seconds")
            self.duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")
        except Exception as e:
            self.notification_var.set(f"Error getting duration: {e}")

    def Frequency_Calculation(self, file_path):
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

            self.audio_samples = audio_samples

            # Perform FFT and find frequencies
            fft_result = np.abs(scipy.fftpack.fft(audio_samples))
            frequencies = np.fft.fftfreq(len(fft_result), d=1 / framerate)

            # Consider only positive frequencies
            positive_freqs = frequencies[:len(frequencies) // 2]
            positive_fft_result = fft_result[:len(fft_result) // 2]

            # Find the dominant frequency
            dominant_frequency = positive_freqs[np.argmax(positive_fft_result)]

            # Update the frequency label in the GUI
            self.frequency_label.config(text=f"Frequency: {dominant_frequency:.2f} Hz")
            self.notification_var.set(f"Calculated Frequency: {dominant_frequency:.2f} Hz")

        except Exception as e:
            self.notification_var.set(f"Error in frequency calculation: {e}")

    def RT60LOW_Calculation(self, file_path):
        """
        Calculates the RT60 Low value of the .wav file and updates the rt60_low_label.
        """
        try:
            audio_samples = self.audio_samples

            # Simulated RT60 Low calculation (using simple decay analysis for demonstration)
            # Assume low frequencies are the first 20% of the FFT spectrum
            fft_result = np.abs(scipy.fftpack.fft(audio_samples))
            low_freq_fft = fft_result[:len(fft_result) // 5]  # First 20% frequencies

            # Estimate decay time (this is a placeholder; real RT60 would use a more complex model)
            rt60_low_value = np.mean(low_freq_fft) / max(low_freq_fft) * 1000  # Placeholder scaling

            # Update the label in the GUI
            self.rt60_low_label.config(text=f"RT60 Low: {rt60_low_value:.2f} ms")
            self.notification_var.set(f"RT60 Low Calculated: {rt60_low_value:.2f} ms")

        except Exception as e:
            self.notification_var.set(f"Error in RT60 Low calculation: {e}")

    def RT60MID_Calculation(self, file_path):
        """
        Calculates the RT60 Mid value of the .wav file and updates the rt60_mid_label.
        """
        try:
            audio_samples = self.audio_samples

            # Simulated RT60 Mid calculation (using simple decay analysis for demonstration)
            # Assume mid frequencies are between 20% and 60% of the FFT spectrum
            fft_result = np.abs(scipy.fftpack.fft(audio_samples))
            mid_freq_fft = fft_result[len(fft_result) // 5 : len(fft_result) * 3 // 5]  # 20% to 60% frequencies

            # Estimate decay time (this is a placeholder; real RT60 would use a more complex model)
            rt60_mid_value = np.mean(mid_freq_fft) / max(mid_freq_fft) * 1000  # Placeholder scaling

            # Update the label in the GUI
            self.rt60_mid_label.config(text=f"RT60 Mid: {rt60_mid_value:.2f} ms")
            self.notification_var.set(f"RT60 Mid Calculated: {rt60_mid_value:.2f} ms")

        except Exception as e:
            self.notification_var.set(f"Error in RT60 Mid calculation: {e}")

    def RT60HIGH_Calculation(self, file_path):
        """
        Calculates the RT60 High value of the .wav file and updates the rt60_high_label.
        """
        try:
            audio_samples = self.audio_samples

            # Simulated RT60 High calculation (using simple decay analysis for demonstration)
            # Assume high frequencies are the last 20% of the FFT spectrum
            fft_result = np.abs(scipy.fftpack.fft(audio_samples))
            high_freq_fft = fft_result[-len(fft_result) // 5:]  # Last 20% frequencies

            # Estimate decay time (this is a placeholder; real RT60 would use a more complex model)
            rt60_high_value = np.mean(high_freq_fft) / max(high_freq_fft) * 1000  # Placeholder scaling

            # Update the label in the GUI
            self.rt60_high_label.config(text=f"RT60 High: {rt60_high_value:.2f} ms")
            self.notification_var.set(f"RT60 High Calculated: {rt60_high_value:.2f} ms")

        except Exception as e:
            self.notification_var.set(f"Error in RT60 High calculation: {e}")

    def display_waveform(self, file_path):
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
            for widget in self.waveform_frame.winfo_children():
                widget.destroy()

            # Embed the plot in the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.waveform_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.notification_var.set("Waveform displayed.")
        except Exception as e:
            self.notification_var.set(f"Error displaying waveform: {e}")

    def display_rt60(self, type_freq):
        try:
            # Clear existing widgets in the frame
            for widget in self.waveform_frame.winfo_children():
                widget.destroy()

            # Convert audio data to numpy array
            audio_samples = self.audio_samples

            # Create the waveform plot with a larger figure size
            fig, ax = plt.subplots(figsize=(12, 6))  # Adjusted figure size

            fft_result = np.abs(scipy.fftpack.fft(audio_samples))

            #Tests if the type of frequency required is low
            if type_freq == "low":
                low_freq_fft = fft_result[:len(fft_result) // 5]  # First 20% frequencies
                time = np.linspace(0, len(low_freq_fft), len(low_freq_fft))
                ax.plot(time, low_freq_fft, color="blue")
                ax.set_title("RT60 Low Frequency", fontsize=16)

            elif type_freq == "medium":
                mid_freq_fft = fft_result[len(fft_result) // 5 : len(fft_result) * 3 // 5]  # 20% to 60% frequencies
                time = np.linspace(0, len(mid_freq_fft), len(mid_freq_fft))
                ax.plot(time, mid_freq_fft, color="blue")
                ax.set_title("RT60 Medium Frequency", fontsize=16)

            elif type_freq == "high":
                high_freq_fft = fft_result[-len(fft_result) // 5:]  # Last 20% frequencies
                time = np.linspace(0, len(high_freq_fft), len(high_freq_fft))
                ax.plot(time, high_freq_fft, color="blue")
                ax.set_title("RT60 High Frequency", fontsize=16)

            ax.set_xlabel("Time (s)", fontsize=12)
            ax.set_ylabel("Amplitude (dB)", fontsize=12)
            ax.grid(True)  # Optional: Add a grid for better readability

            # Embed the plot in the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.waveform_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.notification_var.set("Waveform displayed.")
        except Exception as e:
            self.notification_var.set(f"Error displaying waveform: {e}")


######################################################################################

if __name__ == "__main__":
    SPIDAM = tk.Tk()
    app = audioLoader(SPIDAM)
    SPIDAM.mainloop()