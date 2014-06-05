#!/usr/bin/env python

import mytools as mt
import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np

class ButterflyGUI(QtGui.QMainWindow):
	def __init__(self,analyzefcn,infile=None):
		# ======================================
		# Save default info
		# ======================================
		self.analyzefcn = analyzefcn
		self.infile=infile

		# ======================================
		# Initialize class
		# ======================================
		QtGui.QMainWindow.__init__(self)
	
		# ======================================
		# Use QT Designer window
		# ======================================
		self.ui = mw.Ui_MainWindow()
		self.ui.setupUi(self)


		# ======================================
		# Connect "Redo Analysis" button
		# ======================================
		self.ui.analyzebtn.clicked.connect(self.run_sim)

		# ======================================
		# Load file passed in
		# ======================================
		if self.infile != None:
			self.camname = infile['camname']
			self.camname = mt.derefstr(self.camname)
			self.imgnum = infile['imgnum'][0,0]
			self.loadfile(camname=self.camname,imgnum=self.imgnum)

		self.ui.imageview_mpl.setSliderValue(3600)

		# ======================================
		# Connect camname_combobox
		# ======================================
		self.ui.camname_combobox.currentIndexChanged.connect(self.camname_combobox_changed)

		# ======================================
		# Connect camname_combobox
		# ======================================
		# Disable tracking
		self.ui.imagenum_slider.setTracking(False)
		self.ui.imagenum_slider.valueChanged.connect(self.imagenum_slider_changed)

	def imagenum_slider_changed(self,val=None):
		if val!=None:
			self.imgnum=val
		# self.setup_imagenum_slider(self.infile,img_num=self.imgnum)
		print 'Image number is {}'.format(self.imgnum)

		imgstr = self.data['raw']['images'][str(self.camname)]
		# uids = imgstr['UID']
		# uids = uids[self.imgnum-1]
		# self.oimg   = mt.E200.E200_load_images(imgstr,self.infile,uids)
		self.oimg   = self.allimgs[self.imgnum-1]
		if self.camname=='ELANEX':
			self.oimg = np.rot90(self.oimg)
		self.ui.imageview_mpl.image = self.oimg
		# self.ui.imageview_mpl.setSliderValue(3600)
		
		rect = self.ui.imageview_mpl.rect
		if self.camname=='CMOS_FAR':
			x0 = 275
			x1 = 325
			y0 = 1870
			y1 = 1900
			border=250
		elif self.camname=='ELANEX':
			print 'Elanex'
			x0=0 + 50
			x1=self.ui.imageview_mpl.image.shape[0] - 50
			y0=0 + 50
			y1=self.ui.imageview_mpl.image.shape[1] - 50
			border=50
			
		rect.set_width(y1 - y0)
		rect.set_height(x1 - x0)
		rect.set_xy((y0, x0))

		self.ui.imageview_mpl.zoom_rect(border=border)
		# self.run_sim()

	def camname_combobox_changed(self):
		self.camname=self.ui.camname_combobox.currentText()
		self.allimgs=self.loadimages()
		self.imagenum_slider_changed()
		print 'Tracking is {}'.format(self.ui.imagenum_slider._tracking)

	def loadimages(self):
		# Load images
		imgstr=self.data['raw']['images'][str(self.camname)]
		uids = imgstr['UID']
		return mt.E200.E200_load_images(imgstr,self.infile,uids)

	def loadfile(self,camname=None,imgnum=1):
		if camname==None:
			camname=self.ui.camname_combobox.currentText()
		self.camname = camname
	
		self.imgnum = imgnum
		self.data   = self.infile['data']

		self.allimgs = self.loadimages()
		# self.oimg   = self.oimg[0]

		# Set cameras per infile
		self.set_camnames(self.infile,camname=self.camname)

		# self.ui.imagenum_slider.setValue(self.imgnum)
		self.setup_imagenum_slider(self.infile,imgnum)
		self.imagenum_slider_changed()
		print 'Finished loading'

	def set_camnames(self,infile,camname=None):
		camnames = np.array(infile['data']['raw']['images'].keys())
		self.ui.camname_combobox.clear()
		self.ui.camname_combobox.addItems(camnames)
		self.camnames = camnames

		if camname!=None:
			# camname=str(camname)
			camname_index = np.where(self.camnames==camname)
			self.ui.camname_combobox.setCurrentIndex(camname_index[0])

	def setup_imagenum_slider(self,f,imgnum=1):
		camname = str(self.ui.camname_combobox.currentText())
		numimgs = f['data']['raw']['images'][camname]['UID'].shape[0]
		print 'Number of images is {}'.format(numimgs)
		self.ui.imagenum_slider.setMinimum(1)
		self.ui.imagenum_slider.setMaximum(numimgs)
		self.ui.imagenum_slider.setValue(imgnum)

	def gaussfit_update(self,val):
		ax=self.ui.gaussfit_mpl.ax
		ax.clear()
		gauss_result = self.gaussresults[val-1]
		gauss_result.plot(ax)
		ax.set_title('Gauss Fit, Slice {}'.format(val))

		ax.figure.canvas.draw()

	def run_sim(self):
		print 'Clicked!'
		self.ui.fitview_mpl.ax.clear()
		self.ui.roiview_mpl.ax.clear()
		self.gaussresults = self.analyzefcn(f=self.infile,
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

		self.ui.gaussfit_slider.setMinimum(1)
		self.ui.gaussfit_slider.setMaximum(self.gaussresults.shape[0])
		self.ui.gaussfit_slider.valueChanged.connect(self.gaussfit_update)
		self.gaussfit_update(1)

	# def slider_change(self,val,name):
	#         getattr(self.ui,name).setText(str(val))

	def updateROI(self,rect):
		img=self.oimg[xstart:xstop,ystart:ystop]

