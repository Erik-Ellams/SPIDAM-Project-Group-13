'''from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

wav_fname = '16bit4chan.wav'
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")
'''


'''time = np.linspace(0., length, data.shape[0])
print(time)
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()'''

'''
wavelength = 0
velocity = 0
frequency = 0
r_freq = 0'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

wav_file_name = "16bit4chan.wav"
sample_rate, data = wavfile.read(wav_file_name)

def find_targ_freq(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x

def freq_check():
    global target_freq
    target_freq = find_targ_freq(freqs)
    index_of_freq = np.where(freqs == target_freq)[0][0]
