#!/usr/bin/env python

import mytools as mt
import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np

def temp():
	print 'heyo'

# class ButterflyGUI(mw.Ui_MainWindow):
#     def __init__(self, parent=None, name=None, fl=0):
#         mw.__init__(self,parent,name,fl)

# app = QtGui.QApplication(sys.argv)

class ButterflyGUI(QtGui.QMainWindow):
	def __init__(self,analyzefcn,infile=None):
		self.analyzefcn = analyzefcn
		self.infile=infile
		QtGui.QMainWindow.__init__(self)
	
		self.ui = mw.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.analyzebtn.clicked.connect(self.run_sim)
		self.ui.leftpoint_slider.valueChanged.connect(lambda val: self.slider_change(val,'leftpoint_text'))
		self.ui.rightpoint_slider.valueChanged.connect(lambda val: self.slider_change(val,'rightpoint_text'))

		if infile != None:
			data   = infile['data']
			imgnum = infile['imgnum'][0,0]
			print 'Image number is {}.'.format(imgnum)
			camname = infile['camname']
			camname = mt.derefstr(camname)
			imgstr = data['raw']['images'][camname]
			oimg   = mt.E200.E200_load_images(imgstr,infile)
			oimg   = oimg[imgnum-1,:,:]
			imgplot = self.ui.imageview_mpl.ax.imshow(oimg,interpolation='none')
			imgplot.set_clim(0,3600)

			self.ui.imageview_mpl.fig.colorbar(imgplot)

			rect = self.ui.imageview_mpl.rect
			x0 = 275
			x1 = 325
			y0 = 1870
			y1 = 1900
			rect.set_width(y1 - y0)
			rect.set_height(x1 - x0)
			rect.set_xy((y0, x0))
			print rect

			self.ui.imageview_mpl.zoom_rect(border=50)
			

	def run_sim(self):
		print 'Clicked!'
		self.analyzefcn(f=self.infile,rect=self.ui.imageview_mpl.rect)

	def slider_change(self,val,name):
		# print 'Slider is at {}'.format(val)
		getattr(self.ui,name).setText(str(val))

