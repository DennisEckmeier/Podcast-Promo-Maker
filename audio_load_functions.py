# -*- coding: utf-8 -*-
"""
Functions to import and prepare audio data for Podcast Promo Maker

Created on Thu Aug 30 09:43:31 2018

@author: Dennis Eckmeier
"""

import scipy.io.wavfile as wave
import numpy as np

def get_audio_wave(audio):
    audio['rate'], audio['wave'] = wave.read(audio['filename'])
    if len(audio['wave'].shape) == 1:
        audio['nSamples'], = audio['wave'].shape
        audio['nChannels'] = 1
    elif len(audio['wave'].shape) == 2:
        audio['nSamples'], audio['nChannels'] = audio['wave'].shape
        
    audio['wave'] = audio['wave'] / np.max(np.abs(audio['wave']))
    return audio

