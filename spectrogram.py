import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

def get_data(fp):
    samprate, data = wavfile.read(fp)
    assert samprate == 16000
    assert len(data.shape) == 1
    assert data.dtype == np.dtype('int16')
    return samprate, data

def spectrogram(fp, period_secs = 0.5):
    sample_rate, samples = get_data(fp)
    frequencies, times, spectrogram = signal.spectrogram(samples, period_secs*sample_rate)
    return frequencies, times, spectrogram

if __name__ == '__main__':
    fp = 'Katey_Sagal/4HvcwvtDLKw_0000001.wav'
    frequencies, times, spectrogram = spectrogram(fp)
    plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower')
    plt.show()

