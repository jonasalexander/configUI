'''
This file handles all the configuration of the interface 
style from font to colors etc.
All such configurations that are necessarily implemented in 
other files are marked with a '# GRAPHICS' comment.
'''

from Tkinter import *
import tkFont

# Returns a font of type Source Sans Pro. Size & 
# window for which font is valid set as parameters
def getBigRepFont(window, size):
	return tkFont.Font(window, ("Source Sans Pro", size, NORMAL))

def centerWindow(window):
	window.update()

	h = window.winfo_height()
	w = window.winfo_width()

	# get screen width and height
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()

	# calculate x and y coordinates for the Tk root window
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	# set the dimensions of the screen and where it is placed
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))

