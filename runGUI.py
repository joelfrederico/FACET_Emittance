#!/usr/bin/env python #-m pdb

# import sys
# from IPython.core import ultratb
# sys.excepthook = ultratb.FormattedTB(mode='Verbose',
# color_scheme='Linux', call_pdb=1)

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
from save_analysis import save_analysis

def runGUI(filename,camname,imgnum,verbose=False,loglevel=0):
	# ======================================
	# Set up logging
	# ======================================
	logger = mt.mylogger(filename='runGUI')

	# ======================================
	# Load data and run program
	# ======================================

	data=E200.E200_load_data(filename)
	
	# Generate or retrieve qt app
	app = mt.qt.get_app()

	window = ButterflyGUI(
			analyzefcn = analyze_matlab ,
			savefcn    = save_analysis  ,
			dataset    = data           ,
			camname    = camname        ,
			imgnum     = imgnum         ,
			verbose    = verbose
			)
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
