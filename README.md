# Podcast Promo Maker
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

# Settings
In the script file you will find the following section, some of which you need to modify, some of which you may modify, and some of which you should not touch:

audio = {'filename':'outro.wav',                         # HERE GOES THE NAME OF THE INPUT AUDIO FILE (must be WAV)
         'volume':'14dB',                                YOU MAY CHANGE THE VOLUME IF YOU LIKE
         'bitrate':'128k',                               DON'T CHANGE (social media compliance)  
         'codec':'aac'}                                  DON'T CHANGE (social media compliance)

bkg_filename = 'tardi.png'
au_plot = {'height':60,'Ypos':560,'nChan':1}             CHANGE POSITION AND HEIGHT OF THE AUDIO WAVE PLOT
new_vid = {'filename':'sfp_podcast.mp4',                 # HERE GOES THE NAME OF THE *OUTPUT* FILE
           'fps':30,                                     DON'T CHANGE (social media compliance)  
           'size':[640,640],                             DON'T CHANGE (social media compliance)  
           'dpi':150,                                    DON'T CHANGE (social media compliance)  
           'codec':'h264',                               DON'T CHANGE (social media compliance)  
           'bitrate':1024}                               DON'T CHANGE (social media compliance)  

metadata = dict(title='Movie Test',                      # YOU SHOULD ADJUST YOUR VIDEO METADATA
                artist='Matplotlib',
                comment='Movie support!')
text_p = {'xpos':320,                                    # TEXT POSITION
          'ypos':10,
          'text':'Science for Societal Progress',        # TEXT
          'color':'w',                                   # COLOR AND FORMATTING:
          'fontname':'Arial',
          'weight':'heavy',
          'size':'18',
          'horizontalalignment':'center',
          'verticalalignment':'top'}

