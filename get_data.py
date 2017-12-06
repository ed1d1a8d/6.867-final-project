import os, sys
from notebooks.utils import spectrogram
import random

VCB_PATH = "/home/ubuntu/data/voxceleb1_wav"
def get_names_and_clip_paths():
    global VCB_PATH
    names = [d for d in os.listdir(VCB_PATH) if os.path.isdir(os.path.join(VCB_PATH, d))]

    audio_clip_paths = {}
    for name in names:
        audio_clip_paths[name] = os.listdir(VCB_PATH + '/' + name)

    names = sorted(names, key=lambda name : -len(audio_clip_paths[name]))

    return names, audio_clip_paths

NUM_PEOPLE = 10
AUDIO_LENGTH = 128 * 3 # Around 128 columns in spectrogram is one second
AUDIO_GAP = 128 // 2 # Gap of half a second

def get_audio_and_speakers(names, audio_clip_paths):
    """Generate spectrogram for each of the audio clips
    for each name. Returns list of spectrograms and list
    of IDs for their corresponding names in random order.
    """
    global NUM_PEOPLE, AUDIO_LENGTH, AUDIO_GAP

    audio_speakers = []
    for idx, name in enumerate(names[:NUM_PEOPLE]):
        print('Generating spectrograms for', name)
        for audio_clip in audio_clip_paths[name]:
            base_spec = spectrogram.get_spectrogram('/'.join([VCB_PATH, name, audio_clip]))
            length = base_spec.shape[1]
            for start in range(0, length - AUDIO_LENGTH + 1, AUDIO_GAP):
                spec = base_spec[:, start : start + AUDIO_LENGTH]
                audio_speakers.append((spec, idx))

    random.shuffle(audio_speakers)
    audio, speakers = zip(*audio_speakers)
    return audio, speakers
