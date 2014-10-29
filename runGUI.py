#!/usr/bin/env python
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import matplotlib as mpl
mpl.rcParams['image.aspect'] = 'auto'

import E200
import argparse
import h5py as h5
import logging
import mytools as mt
import numpy as np
from ButterflyGUI import ButterflyGUI
from analyze_matlab import analyze_matlab

def runGUI(filename,camname,imgnum,verbose=False,loglevel=0):
	# ======================================
	# Set up logging
	# ======================================
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	fmtr = mt.classes.IndentFormatter(indent_offset=8)
	fmtr_msgonly = mt.classes.IndentFormatter('%(indent)s%(message)s')

	debugh = logging.FileHandler(filename='debug.log',mode='w')
	debugh.setLevel(logging.ERROR)
	debugh.setFormatter(fmtr_msgonly)
	logger.addHandler(debugh)

	ch = logging.StreamHandler()
	if loglevel == 'debug':
		ch.setLevel(logging.DEBUG)
	elif loglevel == 'info':
		ch.setLevel(logging.INFO)
	elif loglevel == 'warning':
		ch.setLevel(logging.WARNING)
	elif loglevel == 'critical':
		ch.setLevel(logging.CRITICAL)
	ch.setFormatter(fmtr_msgonly)
	logger.addHandler(ch)

	fh = logging.FileHandler(filename='runGUI.log',mode='w')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(fmtr)
	logger.addHandler(fh)

	# ======================================
	# Load data and run program
	# ======================================

	data=E200.E200_load_data(filename)
	
	# Generate or retrieve qt app
	app = mt.qt.get_app()

	window = ButterflyGUI(analyze_matlab,data,camname,imgnum,verbose=verbose)
	# img = np.random.randn(10,10)
	# window = ButterflyGUI(analyze_matlab,image=img)
	# window.ui.imageview_mpl.img.image=img
	window.show()
	app.exec_()

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Loads and runs a gui to analyze saved spectrometer data.')
	parser.add_argument('-v','--verbose',action='store_true',
			help='enable verbose mode')
	parser.add_argument('-l','--log',default='info',choices=['debug','info','warning','error','critical'],
			help='increase logging level')
	parser.add_argument('-f','--file',
			help='file to process')
	parser.add_argument('-c','--camera',
			help='camera name')
	parser.add_argument('-i','--imgnum',type=int,
			help='image number')

	arg=parser.parse_args()

	runGUI(arg.file,arg.camera,arg.imgnum,verbose=arg.verbose,loglevel=arg.log)
