# Podcast Promo Maker
Dennis Eckmeier, 2018

The Podcast Promo Maker V0.0.4 creates a simple promo video for a podcast for 
social media. The output is formatted and encoded so it fits recommendations 
by Facebook, Twitter, and Instagram (also works for Pinterest):

    - max duration 60 s
    - video: MP4 (H.264), 30 fps, 1024k bitrate, 640x640 Px
    - audio: AAC (Low Complexity), 64k mono, 128k stereo

## Dependencies:

    - Python 3.7
    - FFMpeg (added to PATH)
    - numpy
    - scipy
    - matplotlib
    - PIL

Developed under Windows 10

## Settings
In the script file you will find the following section, some of which you need to modify, some of which you may modify, and some of which you should not touch:

***audio*** settings dictionary:
--------------------------------------------------------------------------
**filename** key:   **name of the source wav file**
    
**volume** key:     volume of the sound output (default: '14dB')
    
*bitrate* key:      sound compression (default: '128k')
    
*codec* key:        sound codec (default:'aac')

--------------------------------------------------------------------------
***bkg_filename***      **name of the background image file**

--------------------------------------------------------------------------

***au_plot*** dictionary (settings for the audio wave plots):
--------------------------------------------------------------------------
**height** key:     height of the wave plot in the image

**Ypos** key:       Position of plot origin along the **inverted y axis**

*nChan*:            number of channels to plot (doesn't do anything atm)

--------------------------------------------------------------------------

***new_vid*** dictionary:
--------------------------------------------------------------------------
**filename** key:   **name of the output file**

*fps* key:          output video frame rate (default:30)

*size* key:         output dimension in px: (default: [640,640])

*dpi* key:          figure resolution (default:150)

*codec* key:        output video mp3 codec (default:'h264')

*bitrate* key:      output video compression bitrate (default:1024)

--------------------------------------------------------------------------

***metadata***
--------------------------------------------------------------------------
**title** key:      The title of the episode.

**artist** key:     your name

**comment** key:    Your opportunity to mention Podcast Promo Maker!

--------------------------------------------------------------------------
***text_p*** dictionary
--------------------------------------------------------------------------
**xpos** and **ypos** keys:  x and y position of the text **(inverted y axis!)**

**text** key:        the text.

**color**, **fontname**, **weight**, **size, **horizontalalignment**, and **verticalalignment** are formatting settings (see matplotlib.pyplot.text())

--------------------------------------------------------------------------
