#!/usr/bin/env python
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import argparse

import mytools as mt
from ButterflyGUI import ButterflyGUI
from analyze_matlab import analyze_matlab
import h5py as h5
import matplotlib as mpl
mpl.rcParams['image.aspect'] = 'auto'
import numpy as np
import logging

def runGUI(filename,camname,imgnum,verbose=False,loglevel=0):
	# ======================================
	# Set up logging
	# ======================================
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler(filename='runGUI.log',mode='w')
	fh.setLevel(logging.DEBUG)

	debugh = logging.FileHandler(filename='debug.log',mode='w')
	debugh.setLevel(logging.ERROR)

	ch = logging.StreamHandler()
	if loglevel == 'debug':
		ch.setLevel(logging.DEBUG)
	elif loglevel == 'info':
		ch.setLevel(logging.INFO)
	elif loglevel == 'warning':
		ch.setLevel(logging.WARNING)
	elif loglevel == 'critical':
		ch.setLevel(logging.CRITICAL)

	fmtr = logging.Formatter('%(levelname)s - %(name)s:%(funcName)s%(lineno)d\n%(message)s\n')
	fmtr_msgonly = logging.Formatter('%(message)s\n')

	fh.setFormatter(fmtr)
	ch.setFormatter(fmtr_msgonly)
	debugh.setFormatter(fmtr_msgonly)

	logger.addHandler(fh)
	logger.addHandler(ch)
	logger.addHandler(debugh)


	data=mt.E200.E200_load_data(filename)
	
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
