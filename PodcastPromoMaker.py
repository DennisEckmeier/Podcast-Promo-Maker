# -*- coding: utf-8 -*-
"""
The Podcast Promo Maker V0.0.4 creates a simple promo video for a podcast for 
social media. The output is formatted and encoded so it fits recommendations 
by Facebook, Twitter, and Instagram (also works for Pinterest):

    - max duration 60 s
    - video: MP4 (H.264), 30 fps, 1024k bitrate, 640x640 Px
    - audio: AAC (Low Complexity), 64k mono, 128k stereo

Dependencies:
    - Python 3.7
    - FFMpeg (added to PATH)
    - numpy
    - scipy
    - matplotlib
    - PIL

Developed under Windows 10

Created on Thu Aug 23 17:31:12 2018
@author: Dennis Eckmeier


"""

# -----------------------------------------------------------------------
# Parameters to adjust (* = change not recommended)

# -----------------------------------------------------------------------

# imports
from subprocess import call
import os
import sys
import numpy as np
from matplotlib.animation import FFMpegWriter
from PIL import Image
import audio_load_functions as ppm_alf
from parse_arguments import parse_arguments

# --

# prep functions:
def read_sound_file(audio):
    audio = ppm_alf.get_audio_wave(audio)
    return audio

def get_background_image(bkg_filename,new_vid):
    img_obj = Image.open(bkg_filename)
    i = np.argmin(np.abs(np.subtract(img_obj.size,tuple(new_vid['size']))))
    nwidth,nheight = new_vid['size']
    if i == 0:
        nheight = int(np.round(new_vid['size'][0] * (img_obj.size[1]/img_obj.size[i])))
    elif i == 1:
        nwidth = int(np.round(new_vid['size'][1] * (img_obj.size[0]/img_obj.size[i])))
    out = img_obj.resize((nwidth,nheight))
    new_im = Image.new("RGB", tuple(new_vid['size']))   ## luckily, this is already black!
    new_im.paste(out, (int(np.round((new_vid['size'][0]-out.size[0])/2)),
                      int(np.round((new_vid['size'][1]-out.size[1])/2)) ))
    return new_im

# Animation Functions
# def anim_init(): - for later use


# --
def podcast_promo_maker(audio, bkg_filename,au_plot,new_vid,metadata,text_p):
    """
    Main function
    """
    
#    
#   PREPARING INPUTS
#    
    audio = read_sound_file(audio)
    new_vid['nFrames'] = int(np.ceil((np.size(audio['wave'])/audio['rate']/audio['nChannels'])*new_vid['fps']))
    au_plot['ind_trans_const'] = (1/new_vid['fps']) * audio['rate']
    im_bkg = get_background_image(bkg_filename,new_vid);
    
    if new_vid['nFrames']/new_vid['fps'] > 60:
        print('Sound is too long. Video will be cut at 60s')
        new_vid['nFrames'] = 60*new_vid['fps']
        #FIX ME: move check into read_sound_file and cut the audio data there!
        
#    
#   MAKE ANIMATION
#
        # choosing the audio visualization style:
    if au_plot['style'] == 'simple_wave':
        import anim_simple_wave as a
    elif au_plot['style'] == 'simple_fbars':
        import anim_simple_frequency_bars as a
        
        # make animation
    ani=a.run_animation(audio,au_plot,new_vid,im_bkg,text_p)
    
#
#   SAVE ANIMATION AS VIDEO
#
    writer = FFMpegWriter(fps=new_vid['fps'], 
                          codec=new_vid['codec'], 
                          bitrate=new_vid['bitrate'], 
                          metadata=metadata)
    ani.save('temp_video.mp4', writer=writer,dpi=new_vid['dpi'])
    
#    
#    ADD THE SOUND
#    
    print('converting wav to mp3 ...')
    cmd = 'ffmpeg -y -i {} -shortest temp_audio.mp3'.format(audio['filename'])
    call(cmd, shell=True)     
    
    print('combining video and audio ...')
    cmd = 'ffmpeg -y -i temp_video.mp4 -i temp_audio.mp3 -filter:a "volume={}"  -c:v {}  -c:a {} -b:a {} -shortest {}'.format(audio['volume'],new_vid['codec'],audio['codec'],audio['bitrate'],new_vid['filename'])
    call(cmd, shell=False)     
    
    os.remove('temp_audio.mp3')
    os.remove('temp_video.mp4')
    
# END OF FUNCTIONS ------------------------------------------

# RUN
audio, bkg_filename,au_plot,new_vid,metadata,text_p = parse_arguments(sys.argv[1:])  
podcast_promo_maker(audio, bkg_filename,au_plot,new_vid,metadata,text_p)