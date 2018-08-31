# -*- coding: utf-8 -*-
"""

simple_wave audio visualization

Created on Fri Aug 31 09:24:43 2018
@author: Dennis Eckmeier
"""

import scipy.signal as sci
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import figure_initialization as fini

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

def initialize_figure(new_vid,im_bkg,text_p):
    
    fig = fini.fig_init(new_vid,im_bkg,text_p)
    fig.add_subplot(111)
    ln1, = plt.plot([], [], 'r', animated=True)
    ln2, = plt.plot([], [], 'r', animated=True)
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    return fig, ln1, ln2

def run_animation(audio,au_plot,new_vid,im_bkg,text_p):
    
    fig,ln1,ln2 = initialize_figure(new_vid,im_bkg,text_p)
    ani = FuncAnimation(fig,
                        anim_update,
                        frames=new_vid['nFrames'],
                        fargs=(au_plot, audio, new_vid,ln1,ln2),
                        blit=True,
                        repeat=False)
    return ani