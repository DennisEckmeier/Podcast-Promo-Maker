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
import scipy.signal as sci
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from PIL import Image
import audio_load_functions as ppm_alf
from parse_arguments import parse_arguments

# --

# prep functions:
def read_sound_file(audio):
    audio = ppm_alf.get_audio_wave(audio)
    return audio

def getBackGroundImage(bkg_filename,new_vid):
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


def anim_update(tframe, au_plot, audio, new_vid,ln1,ln2):
    print('{:.0f} % complete  '.format(tframe/new_vid['nFrames']*100), end='\r')
#    print('frame: {}      '.format(tframe), end='\r')
    au_start = int(round(tframe * au_plot['ind_trans_const']))
    au_end   = int(round(((tframe+1) * au_plot['ind_trans_const']) - 1))
    
    if au_end > audio['nSamples']:
        au_end = audio['nSamples']
    
    tChanHeight = au_plot['height']/au_plot['n_chan']
        
    # Channel1
    au_wave = audio['wave'][range(au_start,au_end),0]
    au_wave = sci.resample(au_wave, new_vid['size'][1])*tChanHeight
    ln1.set_data(list(range(1, new_vid['size'][1]+1)), au_wave+au_plot['ypos'])
    # Channel2
    if audio['nChannels'] == 1:
        au_wave = au_wave+tChanHeight
    else:
        au_wave = audio['wave'][range(au_start,au_end),1]
        au_wave = sci.resample(au_wave, new_vid['size'][1])
        au_wave = au_wave*tChanHeight
    ln2.set_data(list(range(1,new_vid['size'][1]+1)), au_wave+au_plot['ypos']+tChanHeight)
    return ln1,ln2
# --
def podcast_promo_maker(audio, bkg_filename,au_plot,new_vid,metadata,text_p):
    """
    Main function
    """
    # default values:

    # ---
    # PREPARE DATA
    audio = read_sound_file(audio)
    new_vid['nFrames'] = int(np.ceil((np.size(audio['wave'])/audio['rate']/audio['nChannels'])*new_vid['fps']))
    au_plot['ind_trans_const'] = (1/new_vid['fps']) * audio['rate']
    
    if new_vid['nFrames']/new_vid['fps'] > 60:
        print('Sound is too long. Video will be cut at 60s')
        new_vid['nFrames'] = 60*new_vid['fps']
    
    # INITIALIZE FIGURE
    fig = plt.figure(dpi=new_vid['dpi'], figsize=[x/new_vid['dpi'] for x in new_vid['size']])
    plt.imshow(getBackGroundImage(bkg_filename,new_vid),origin='upper')
    plt.text(text_p['xpos'],
             text_p['ypos'],
             text_p['text'],
             color = text_p['color'],
             fontname = text_p['fontname'],
             weight = text_p['weight'],
             size = text_p['size'],
             horizontalalignment=text_p['horizontalalignment'],
             verticalalignment=text_p['verticalalignment'])
    fig.add_subplot(111)
    ln1, = plt.plot([], [], 'r', animated=True)
    ln2, = plt.plot([], [], 'r', animated=True)
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #
    # RUN ANIMATION
    #
    writer = FFMpegWriter(fps=new_vid['fps'], codec=new_vid['codec'], bitrate=new_vid['bitrate'], metadata=metadata)
    
    ani = FuncAnimation(fig,
                        anim_update,
                        frames=new_vid['nFrames'],
                        fargs=(au_plot, audio, new_vid,ln1,ln2),
                        blit=True,
                        repeat=False)
    
    ani.save('temp_video.mp4', writer=writer,dpi=new_vid['dpi'])
#    
#    # ADD THE SOUND
#    
    print('converting wav to mp3 ...')
    cmd = 'ffmpeg -y -i {} -shortest temp_audio.mp3'.format(audio['filename'])
    call(cmd, shell=True)     
    
    print('combining video and audio ...')
    cmd = 'ffmpeg -y -i temp_video.mp4 -i temp_audio.mp3 -filter:a "volume={}"  -c:v {}  -c:a {} -b:a {} -shortest {}'.format(audio['volume'],new_vid['codec'],audio['codec'],audio['bitrate'],new_vid['filename'])
    call(cmd, shell=True)     
    
    os.remove('temp_audio.mp3')
    os.remove('temp_video.mp4')

# END FUNCTIONS

audio, bkg_filename,au_plot,new_vid,metadata,text_p = parse_arguments(sys.argv[1:])
    
podcast_promo_maker(audio, bkg_filename,au_plot,new_vid,metadata,text_p)