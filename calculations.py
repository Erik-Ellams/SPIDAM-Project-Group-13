#ReverbTime1
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment

wav_file_name = "16bit4chan.wav"
sample_rate, data = wavfile.read(wav_file_name)
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

def debugg(fstring):
    print(fstring)

def find_targ_freq(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x

def freq_check():
    #global target_freq
    debugg(f'freqs {freqs[:10]}')
    target_freq = find_targ_freq(freqs)
    debugg(f'target_freq {target_freq}')
    index_of_freq = np.where(freqs == target_freq)[0][0]
    debugg(f'index_of_freq {index_of_freq}')

    data_for_freq = spectrum[index_of_freq]
    debugg(f'data for freq {data_for_freq}')

    data_in_db_fun = 10 * np.log10(data_for_freq)
    return data_in_db_fun

data_in_db = freq_check()
plt.figure()

plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')

index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5

#P4
def find_nearest_value(array, value):
    array = np.asarray(array)
    debugg(f'array {array[:10]}')
    idx = (np.abs(array-value)).argmin()
    debugg(f'idx {idx}')
    debugg(f'array[idx] {array[idx]}')
    return array[idx]

value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)

index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')


value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]

rt60 = 3 * rt20

plt.grid()

plt.show()

print(f'The RT60 reverb is {round(abs(rt60), 2)}')
