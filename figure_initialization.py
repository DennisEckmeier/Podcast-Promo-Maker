# -*- coding: utf-8 -*-
"""

Initialize Animation Figure

Created on Fri Aug 31 10:00:18 2018
@author: denni
"""

import matplotlib.pyplot as plt

def fig_init(new_vid,im_bkg,text_p):
    
    try:
        text_p['text'] = text_p['text'].replace("\\n", "\n")
    except:
        False
    
    fig = plt.figure(dpi=new_vid['dpi'], figsize=[x/new_vid['dpi'] for x in new_vid['size']])
    plt.imshow(im_bkg,origin='upper')
    plt.text(text_p['xpos'],
             text_p['ypos'],
             text_p['text'],
             color = text_p['color'],
             fontname = text_p['fontname'],
             weight = text_p['weight'],
             size = text_p['size'],
             horizontalalignment=text_p['horizontalalignment'],
             verticalalignment=text_p['verticalalignment'])
    return fig