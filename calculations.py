'''from scipy.io import wavfile
import scipy.io

wav_fname = '16bitstereoFX.wav'
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")


import matplotlib.pyplot as plt
import numpy as np
time = np.linspace(0., length, data.shape[0])
numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
axis=0)[source]

import matplotlib.pyplot as plt
import numpy as np
time = np.linspace(0., length, data.shape[0])


import matplotlib.pyplot as plt
import numpy as np
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()'''

'''
NEEDS:
- 
'''