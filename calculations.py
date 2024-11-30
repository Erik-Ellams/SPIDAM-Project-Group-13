from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

wav_fname = '16bit4chan.wav'
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")



time = np.linspace(0., length, data.shape[0])
print(time)
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()


wavelength = 0
velocity = 0
frequency = 0
r_freq = 0