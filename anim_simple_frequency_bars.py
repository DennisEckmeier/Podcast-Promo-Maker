# -*- coding: utf-8 -*-
"""

simple_fbars audio visualization

Created on Thu Aug 30 17:43:39 2018
@author: Dennis Eckmeier
"""
import bisect
import numpy as np
import scipy.fftpack
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import figure_initialization as fini

def anim_update(tframe,y_all,bars,new_vid):
    
    print('{:.0f} % complete  '.format(tframe/new_vid['nFrames']*100), end='\r')
    y_binned = y_all[tframe,:]
    for i, tb in enumerate(bars):
        tb.set_height((y_binned[i]/np.max(y_binned)*30))
    return bars
    
def initialize_figure(new_vid,im_bkg,text_p,au_plot):
    fig = fini.fig_init(new_vid,im_bkg,text_p)
    ax = fig.add_subplot(111)
    barwidth = new_vid['width']/au_plot['nbars']
    barpos   = list(np.arange(0,new_vid['width'],barwidth))
    bars = plt.bar(barpos,np.zeros(au_plot['nbars']), 
                   bottom=au_plot['ypos'], 
                   width=barwidth*au_plot['barwidth'], 
                   align="edge",
                   color=au_plot['barcolor'])
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    return fig, ax, bars

def prep_ttf(audio,new_vid,au_plot):
    N = au_plot['ind_trans_const']
    T = 1/audio['rate']
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    cutoff = bisect.bisect(xf,10000)
    xf = xf[range(0, cutoff)]
    xf = np.power(list(range(1,len(xf)+1)),(1/3))
    y_all = np.zeros([new_vid['nFrames'],au_plot['nbars']],'float')
    y_max = 0
    for tframe in range(0,new_vid['nFrames']):
        au_start = int(round(tframe * au_plot['ind_trans_const']))
        au_end   = int(round(((tframe+1) * au_plot['ind_trans_const']))- 1)
        
        if au_end > audio['nSamples']:
            au_end = audio['nSamples']
        
        if audio['nChannels'] == 1:
            au_wave = audio['wave'][range(au_start,au_end)] 
        else:
            # FIX ME in stereo files, this should be an average of channel 1 and 2
            au_wave = audio['wave'][range(au_start,au_end),0] 
        N = len(au_wave) # Number of samplepoints
        yf = scipy.fftpack.fft(au_wave)
        yf = 2.0/N * np.abs(yf[:N//2])    
        tr = (list(np.arange(1,np.max(xf),np.max(xf)/au_plot['nbars'])))
        y_binned = np.zeros(au_plot['nbars'])
        for i in range(0,len(tr)-1):
            a = np.argmin(abs(xf - tr[i]  ))
            b = np.argmin(abs(xf - tr[i+1]))
            if b > len(yf)-1:
                b = len(yf)-1
            y_binned[i] = np.mean(yf[list(range(a,b))])
        if np.max(y_binned) > y_max:
            y_max = np.max(y_binned) 
            
        y_all[tframe,:] = y_binned
    
    y_all = (y_all / y_max) * au_plot['height']
    return y_all

def run_animation(audio,au_plot,new_vid,im_bkg,text_p):
    
    y_all = prep_ttf(audio,new_vid,au_plot)
    fig, ax, bars = initialize_figure(new_vid,im_bkg,text_p,au_plot)
    ani = FuncAnimation(fig,
                        anim_update,
                        frames=new_vid['nFrames'],
                        fargs=(y_all,bars,new_vid),
                        blit=True,
                        repeat=False)
    return ani