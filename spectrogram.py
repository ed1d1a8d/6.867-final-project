import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


fp = 'Katey_Sagal/4HvcwvtDLKw_0000001.wav'


def get_data(fp):
    samprate, data = wavfile.read(fp)
    assert samprate == 16000
    assert len(data.shape) == 1
    assert data.dtype == np.dtype('int16')
    return samprate, data

def graph_spectrogram(fp):
    data = get_data(fp)
    nfft = 256  # Length of the windowing segments
    fs = 256    # Sampling frequency
    pxx, freqs, bins, im = plt.specgram(data, nfft,fs)
    plt.axis('off')
    plt.savefig('sp_xyz.png',
                dpi=100, # Dots per inch
                frameon='false',
                aspect='normal',
                bbox_inches='tight',
                pad_inches=0) # Spectrogram saved as a .png 


def spectrogram(fp):
    sample_rate, samples = get_data(fp)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    return frequencies, times, spectrogram

if __name__ == '__main__':
    frequencies, times, spectrogram = spectrogram(fp)
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.show()

