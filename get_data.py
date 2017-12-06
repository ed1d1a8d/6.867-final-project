import numpy as np
#import matplotlib.pyplot as plt
import librosa
#import librosa.display

import os, sys

VCB_PATH = "/home/ubuntu/data/voxceleb1_wav"
def get_names_and_clips():
    global VCB_PATH
    names = [d for d in os.listdir(VCB_PATH) if os.path.isdir(os.path.join(VCB_PATH, d))]

    audio_clips = {}
    for name in names:
        audio_clips[name] = os.listdir(VCB_PATH + '/' + name)

    names = sorted(names, key=lambda name : -len(audio_clips[name]))

    return names, audio_clips
    
    #print(names[:10])
    #print(audio_clips[names[0]])


    #audio_path = '/'.join([VCB_PATH, names[0], audio_clips[names[0]][0]])
    #print(audio_path)
    






