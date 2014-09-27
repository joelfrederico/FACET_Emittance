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

def runGUI(filename,camname,imgnum):
	dataset=mt.E200.Data(filename)
	
	# Generate or retrieve qt app
	app = mt.qt.get_app()

	window = ButterflyGUI(analyze_matlab,dataset,camname,imgnum)
	# img = np.random.randn(10,10)
	# window = ButterflyGUI(analyze_matlab,image=img)
	# window.ui.imageview_mpl.img.image=img
	window.show()
	app.exec_()

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Loads and runs a gui to analyze saved spectrometer data.')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('-f','--file',
			help='File to process.')
	parser.add_argument('-c','--camera',
			help='Camera name.')
	parser.add_argument('-i','--imgnum',type=int,
			help='Image number.')

	arg=parser.parse_args()

	runGUI(arg.file,arg.camera,arg.imgnum)
