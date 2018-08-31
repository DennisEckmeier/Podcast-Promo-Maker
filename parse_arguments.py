# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:29:44 2018

@author: Dennis Eckmeier
"""

import sys
import getopt
import configparser as cp


def config_section_values(section,config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            try:
                dict1[option] = int(dict1[option])        
            except:
                try:
                    dict1[option] = float(dict1[option])
                except:
                    False
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def parse_arguments(argv):
    
    try:
        opts, args = getopt.getopt(argv,'a:b:t:v:c:')
    except getopt.GetoptError:
      print('Not all mandatory settings were set.')
      sys.exit(2)    

    # load default configuration
    config = cp.ConfigParser()
    conf_file = 'default_config'

    for opt, arg in opts:
        if opt == '-h':
            f = open('help.txt', 'r')
            print(f.read())
            f.close()
            sys.exit()
        elif opt == '-c':
            conf_file = arg
    
    config.read("{}.ini".format(conf_file))

    
    # Parse arguments:
    audio = config_section_values("audio",config)
    bkg = config_section_values("bkg_filename",config)
    bkg_filename = bkg['filename']
    au_plot = config_section_values("au_plot",config)
    new_vid = config_section_values("new_vid",config)
    new_vid['size']=[new_vid['width'],new_vid['height']]
    metadata = config_section_values("metadata",config)
    text_p = config_section_values("text_p",config)
    
    # applying other settings:
    for opt, arg in opts:
        if opt in ("-a"): 		    #<input audio file>
            audio['filename'] = arg
        elif opt in ("-b"): 		    #<input background image>
            bkg_filename = arg
        elif opt in ("-t"):		        #<episode title>
            text_p['text'] = arg
        elif opt in ("-v"): 		    #<output file name>
            new_vid['filename'] = arg
            
    return audio, bkg_filename,au_plot,new_vid,metadata,text_p
"""            
        [FIX ME]
        elif opt in ("-ap_height"):     #<height of plot in px> (default = 60)
            au_plot['height'] = arg
        elif opt in ("-ap_Y"):          #<y position in px from bottom> (default = 560)
            au_plot['ypos'] = arg
        elif opt in ("-ap_nChan"):      #<number of channels to display> (default = 1)
            au_plot['n_chan'] = arg
        elif opt in ("-ap_style"):      #<choose visualization style> (default = simple_wave)
            au_plot['style'] = arg
        elif opt in ("-t_X"):		    #<x position> (default = 320)
            text_p['xpos'] = arg
        elif opt in ("-t_Y"):		    #<y position from bottom> (default = 10px) 
            text_p['ypos'] = arg
        elif opt in ("-t_col"):		    #<color> (default = 'w')
            text_p['color'] = arg
        elif opt in ("-t_fnt"):		    #<fontname> (default = 'arial')
            text_p['fontname'] = arg
        elif opt in ("-t_wt"):	        #<font weight> (default = 'heavy')
            text_p['weight'] = arg
        elif opt in ("-t_sz"):	        #<font size> (default = 18)
            text_p['size'] = arg
        elif opt in ("-t_horizontal"):  #<horizontal alignment> (default = 'center')
            text_p['horizontalalignement'] = arg
        elif opt in ("-t_vertical"):    #<vertical alignment> (default = 'top')
            text_p['verticalalignement'] = arg
        elif opt in ("-md_title"):      #(default: 'Science for Progress Promo')
            metadata['title'] = arg
        elif opt in ("-md_artist"):     #(default: 'Dennis Eckmeier')
            metadata['artist'] = arg
        elif opt in ("-md_comment"):	#(default: 'www.scienceforprogress.eu')
            metadata['comment'] = arg
        elif opt in ("-a_vol"): 		#<audio volume> (default='12dB')
            audio['volume'] = arg
        elif opt in ("-a_bit"): 		#<audio bitrate> (default='128k')
            audio['bitrate'] = arg
        elif opt in ("-a_cod"): 		#<audio codec> (default='aac')
            audio['codec'] = arg
        elif opt in ("-v_fps"): 		#<video framerate) (default='30')
            new_vid['fps'] = arg
        elif opt in ("-v_fht"):		    #<video frame height in px) (default=640)
            new_vid['size'][1] = arg
        elif opt in ("-v_fwd"):		    #<video frame width in px) (default=640)
            new_vid['size'][0] = arg
        elif opt in ("-v_dpi"): 		#<internally use for window sizing> (default = 150)
            new_vid['dpi'] = arg
        elif opt in ("-v_cod"): 		#<video codec> (default = 'h264')
            new_vid['codec'] = arg
        elif opt in ("-v_bit"): 		#<video compression bitrate> (default = 1024)
            new_vid['bitrate'] = arg
             """
