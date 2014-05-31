#!/usr/bin/env python

import mytools as mt
import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np

class ButterflyGUI(QtGui.QMainWindow):
	def __init__(self,analyzefcn,infile=None):
		self.analyzefcn = analyzefcn
		self.infile=infile
		QtGui.QMainWindow.__init__(self)
	
		self.ui = mw.Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.analyzebtn.clicked.connect(self.run_sim)

		# self.ui.imageview_mpl.img.rectChanged.connect(self.updateROI)

		if infile != None:
			self.data   = infile['data']
			self.imgnum = infile['imgnum'][0,0]
			print 'Image number is {}.'.format(self.imgnum)
			self.camname = infile['camname']
			self.camname = mt.derefstr(self.camname)
			imgstr = self.data['raw']['images'][self.camname]
			uids = imgstr['UID']
			uids = uids[self.imgnum-1]
			self.oimg   = mt.E200.E200_load_images(imgstr,infile,uids)
			self.oimg   = self.oimg[0]
			self.ui.imageview_mpl.image = self.oimg
			self.ui.imageview_mpl.setSliderValue(3600)

			rect = self.ui.imageview_mpl.rect
			x0 = 275
			x1 = 325
			y0 = 1870
			y1 = 1900
			rect.set_width(y1 - y0)
			rect.set_height(x1 - x0)
			rect.set_xy((y0, x0))

			self.ui.imageview_mpl.zoom_rect(border=50)
			
	def run_sim(self):
		print 'Clicked!'
		self.ui.fitview_mpl.ax.clear()
		self.ui.roiview_mpl.ax.clear()
		self.analyzefcn(f=self.infile,
				data=self.data,
				camname=self.camname,
				imgnum=self.imgnum,
				oimg = self.oimg,
				verbose = False,
				roiaxes=self.ui.roiview_mpl.ax,
				plotaxes=self.ui.fitview_mpl.ax,
				rect=self.ui.imageview_mpl.rect)

		self.ui.fitview_mpl.ax.figure.canvas.draw()
		self.ui.roiview_mpl.ax.figure.canvas.draw()

	def slider_change(self,val,name):
		getattr(self.ui,name).setText(str(val))

	def updateROI(self,rect):
		img=self.oimg[xstart:xstop,ystart:ystop]

