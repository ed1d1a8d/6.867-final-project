import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def get_rand_spectrogram_crop(audio_path, crop_length):
    """
    crop_length is in seconds
    """
    y, sr = librosa.load(audio_path, sr=16000)
    length = len(y)
    crop_start = np.random.randint(length - crop_length * sr)
    crop = y[crop_start : crop_start + crop_length * sr]
    S = librosa.feature.melspectrogram(crop, sr=sr, n_mels=128, n_fft=512, hop_length=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    mn = np.min(log_S)
    mx = np.max(log_S)
    log_S -= mn
    log_S /= (mx - mn)
    return log_S

def get_spectrogram(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128, n_fft=512, hop_length=128)
    log_S = librosa.power_to_db(S, ref=np.max)
    mn = np.min(log_S)
    mx = np.max(log_S)
    log_S -= mn
    log_S /= (mx - mn)
    return log_S

def show_spectrogram(audio_path):
    _, sr = librosa.load(audio_path, sr=16000)
    log_S = get_spectrogram(audio_path)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(log_S, sr=sr, hop_length=128, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram')
    plt.colorbar(format='%+02.0f dB')

def show_rand_spectrogram_crop(audio_path, crop_length):
    _, sr = librosa.load(audio_path, sr=16000)
    log_S = get_rand_spectrogram_crop(audio_path, crop_length)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(log_S, sr=sr, hop_length=128, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram')
    plt.colorbar(format='%+02.0f dB')
