#!/usr/bin/env python

import mytools as mt
import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np
import h5py as h5

class ButterflyGUI(QtGui.QMainWindow):
	def __init__(self,analyzefcn,dataset=None,camname=None,imgnum=None,verbose=False):
		# ======================================
		# Save default info
		# ======================================
		self.verbose=verbose
		self.analyzefcn = analyzefcn
		self.dataset = dataset
		self.data=dataset.read_file['data']
		self.infile=dataset.read_file
		self.camname=camname
		self.imgnum=imgnum

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
		# if self.infile != None:
			# self.camname = infile['camname']
			# self.camname = mt.derefstr(self.camname)
			# self.imgnum = infile['imgnum'][0,0]
			# self.loadfile(camname=self.camname,imgnum=self.imgnum)
		if camname==None:
			camname=self.data['raw']['images'].keys()
			camname=camname[0]
		if imgnum==None:
			imgnum=1
		print camname
		print imgnum
		self.loadfile(camname,imgnum)

		self.ui.imageview_mpl.setSliderValue(3600)
		self.ui.imageview_mpl._img.rectChanged.connect(self.saverect)

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

		# ======================================
		# Connect camname_combobox
		# ======================================
		self.ui.imagenum_valid_checkbox.stateChanged.connect(self.updateResults)

		self.ui.saveworld.clicked.connect(self.saveworld)

		# =========================================
		# Configure and Connect plot type selector
		# =========================================
		self.ui.plottype.clear()
		self.plotoptions = np.array([
			['Normalized Emittance', lambda val:val.scanfit.fitresults.emitn],
			['Beta', lambda val:val.scanfit.fitresults.twiss.beta],
			['Beta*', lambda val:val.scanfit.fitresults.twiss.betastar],
			['Alpha', lambda val:val.scanfit.fitresults.twiss.alpha],
			['s*', lambda val:val.scanfit.fitresults.twiss.sstar],
			['MinSpot', lambda val:val.scanfit.fitresults.twiss.minspotsize(val.scanfit.fitresults.emit)],
			['Geometric Emittance',lambda val:val.scanfit.fitresults.emit]
			])
		self.ui.plottype.addItems(self.plotoptions[:,0])
		# self.ui.plottype.addItems(['emit','emitn'])
		self.ui.plottype.currentIndexChanged.connect(self.plotdataset)

	def saverect(self,rect):
		ind = self.ui.imagenum_slider.value-1
		uid = self.allimgs.uid[ind]
		uid = uid[0]
		# print 'UID to save: {:0.0f}'.format(uid)
		processed = self.dataset.write_file['data']['processed']
		vectors = processed['vectors']
		scalars = processed['scalars']
		rect_xy = np.array(rect.get_xy())
		mt.E200.E200_api_updateUID(vectors['rect_xy'],rect_xy,uid)
		mt.E200.E200_api_updateUID(scalars['width'],rect.get_width(),uid)
		mt.E200.E200_api_updateUID(scalars['height'],rect.get_height(),uid)
		self.data.file.flush()
		print 'Saving to index {}, uid {:0.0f}'.format(ind,uid)
		print 'Image number is {}'.format(self.imgnum)
		print rect_xy
		print rect.get_width()
		print rect.get_height()
		print 'saved'

	def plotdataset(self,ind=None):
		if ind==None:
			ind=self.ui.plottype.currentIndex()
		selected_fits=self.fitresults[self.validimg]
		x = np.vectorize(self.plotoptions[ind,1])
		self.ui.dataset_mpl.plot(x(selected_fits))
		print self.plotoptions[ind,0]
		print 'Attempted to plot!'

	def saveworld(self):
		try:
			f = h5.File('data.hdf5','w-')
		except IOError as e:
			if e.message == 'Unable to create file (File exists)':
				f = h5.File('data-{}.hdf5'.format(time.strftime('%Y-%m-%d-%H:%M:%S')),'w-')

		mt.picklejar('mydata.pkl',fitresults=self.fitresults,valid=self.validimg)

	def imagenum_slider_changed(self,val=None):
		# ======================================
		# Set the new image number
		# ======================================
		if val!=None:
			self.imgnum=val
		if self.verbose:
			print 'Image number is {}'.format(self.imgnum)

		# ======================================
		# Open the right image for viewing
		# ======================================
		imgstr = self.data['raw']['images'][str(self.camname)]
		self.oimg   = self.allimgs.images[self.imgnum-1]
		if self.camname=='ELANEX':
			self.oimg = np.rot90(self.oimg)
		self.ui.imageview_mpl.image = self.oimg
		
		# ======================================
		# See if rect info is stored for a UID
		# ======================================
		uid = self.allimgs.uid[self.imgnum-1]
		# Print all UIDs
		if self.verbose:
			for val in self.allimgs.uid:
				print '{:0.0f}'.format(val[0])
		uid = uid[0]
		rect = self.ui.imageview_mpl.rect
		processed = self.dataset.write_file['data']['processed']
		vectors = processed['vectors']
		scalars = processed['scalars']
		rect_info_exists = ('rect_xy' in vectors.keys() and 'width' in scalars.keys() and 'height' in scalars.keys())

		# ======================================
		# Try to load rect info from file
		# ======================================
		use_loaded_rect=False
		if rect_info_exists:
			rect_xy = mt.E200.E200_api_getdat(vectors['rect_xy'],uid).dat
			width   = mt.E200.E200_api_getdat(scalars['width'],uid).dat
			height  = mt.E200.E200_api_getdat(scalars['height'],uid).dat
			# One element each for rect_xy, width, height
			if np.size(rect_xy) == 2 and np.size(width) == 1 and np.size(height) == 1:
				print 'loading rect from file'
				rect_xy = rect_xy[0]
				width   = width[0]
				height  = height[0]

				print 'Uid loaded is {:0.0f}'.format(uid)
				print 'Image number is {}'.format(self.imgnum)

				use_loaded_rect=True

			# if self.camname=='CMOS_FAR':
			# 	border = None
			# 	border_px = 250
			# elif self.camname=='ELANEX':
			# 	border = None
			# 	border_px = 50
			border = np.array([width,height])*0.1
			border_px = None

		# ======================================
		# If unsuccessful, calculate rect info
		# ======================================
		if not use_loaded_rect:
			print 'replacing rect'
			if self.camname=='CMOS_FAR':
				x0     = 275
				x1     = 325
				y0     = 1870
				y1     = 1900
				border = None
				border_px = np.array([250,250])
			elif self.camname=='ELANEX':
				print 'Elanex'
				x0     = 0 + 50
				x1     = self.ui.imageview_mpl.image.shape[0] - 50
				y0     = 0 + 50
				y1     = self.ui.imageview_mpl.image.shape[1] - 50
				border = None
				border_px = np.array([50,50])
			rect_xy = np.array([y0, x0])
			width   = (y1 - y0)
			height  = (x1 - x0)

			if not 'rect_xy' in vectors.keys():
				vectors.create_group('rect_xy')
			if not 'width' in scalars.keys():
				scalars.create_group('width')
			if not 'height' in scalars.keys():
				scalars.create_group('height')
			mt.E200.E200_api_updateUID(vectors['rect_xy'],rect_xy,uid)
			mt.E200.E200_api_updateUID(scalars['width'],width,uid)
			mt.E200.E200_api_updateUID(scalars['height'],height,uid)
			processed.file.flush()

		# ======================================
		# Set and draw rect
		# ======================================
		if self.verbose:
			print rect_xy
			print width
			print height
		rect.set_xy(rect_xy)
		rect.set_width(width)
		rect.set_height(height)

		self.ui.imageview_mpl.zoom_rect(border=border,border_px=border_px)
		self.ui.imagenum_valid_checkbox.setChecked(self.validimg[self.imgnum-1])
		self.ui.imageview_mpl.ax.figure.canvas.draw()

	def camname_combobox_changed(self):
		self.camname=self.ui.camname_combobox.currentText()
		self.allimgs=self.loadimages()
		self.imagenum_slider_changed()
		print 'Tracking is {}'.format(self.ui.imagenum_slider._tracking)

	def loadimages(self):
		# Load images
		imgstr=self.data['raw']['images'][str(self.camname)]
		uids = imgstr['UID']
		return mt.E200.E200_load_images(imgstr,uids)

	def loadfile(self,camname=None,imgnum=1):
		if camname==None:
			camname=self.ui.camname_combobox.currentText()
		self.camname = camname
	
		self.imgnum = imgnum

		self.allimgs = self.loadimages()

		# Set cameras per infile
		self.set_camnames(self.infile,camname=self.camname)

		numimgs = self.infile['data']['raw']['images'][camname]['UID'].shape[0]
		print 'Number of images is {}'.format(numimgs)
		self.ui.imagenum_slider.setMinimum(1)
		self.ui.imagenum_slider.setMaximum(numimgs)
		self.ui.imagenum_slider.setValue(imgnum)

		# =====================================
		# Set arrays for storing fit data
		# =====================================
		self.validimg = np.zeros(numimgs,dtype=np.bool)
		self.fitresults = np.empty(numimgs,dtype=object)

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

	# def setup_imagenum_slider(self,f,imgnum=1):

	def gaussfit_update(self,val):
		ax=self.ui.gaussfit_mpl.ax
		ax.clear()
		gauss_result = self.out.gaussfits[val-1]
		gauss_result.plot(ax)
		ax.set_title('Gauss Fit, Slice {}'.format(val))

		ax.figure.canvas.draw()

	def run_sim(self):
		# =====================================
		# Run the sim
		# =====================================
		print 'Running sim!'
		self.ui.fitview_mpl.ax.clear()
		self.ui.roiview_mpl.ax.clear()
		self.out = self.analyzefcn(f=self.infile,
				data=self.data,
				camname=self.camname,
				imgnum=self.imgnum,
				oimg = self.oimg,
				verbose = False,
				roiaxes=self.ui.roiview_mpl.ax,
				plotaxes=self.ui.fitview_mpl.ax,
				rect=self.ui.imageview_mpl.rect)

		# =====================================
		# Redraw results boxes
		# =====================================
		self.ui.fitview_mpl.ax.figure.canvas.draw()
		self.ui.roiview_mpl.ax.figure.canvas.draw()

		self.ui.gaussfit_slider.setMinimum(1)
		self.ui.gaussfit_slider.setMaximum(self.out.gaussfits.shape[0])
		self.ui.gaussfit_slider.valueChanged.connect(self.gaussfit_update)
		self.gaussfit_update(1)

		# =====================================
		# Save results locally
		# =====================================
		ind = self.ui.imagenum_slider.value-1
		self.fitresults[ind] = self.out

		# =====================================
		# Update emittance plot
		# =====================================
		self.updateEmitPlot()

		# =====================================
		# Extract results to save from classes
		# =====================================
		scanfit = self.out.scanfit
		emit_n = scanfit.fitresults.emitn
		betastar = scanfit.fitresults.Beam.betastar
		sstar = scanfit.fitresults.Beam.sstar

		# =====================================
		# Write results to file
		# =====================================
		ind = self.ui.imagenum_slider.value-1
		uid = self.allimgs.uid[ind]
		uid = uid[0]

		processed = self.dataset.write_file['data']['processed']
		# vectors = processed['vectors']
		scalars = processed['scalars']
		mt.create_group(scalars,'ss_emit_n')
		mt.create_group(scalars,'ss_betastar')
		mt.create_group(scalars,'ss_sstar')
		mt.E200.E200_api_updateUID(scalars['ss_emit_n'],emit_n,uid)
		mt.E200.E200_api_updateUID(scalars['ss_betastar'],betastar,uid)
		mt.E200.E200_api_updateUID(scalars['ss_sstar'],sstar,uid)

		scalars.file.flush()

	def updateEmitPlot(self):
		validresults = self.fitresults[self.validimg]
		self.emit = np.empty(validresults.shape[0])
		print validresults
		print validresults.shape
		print type(validresults)
		for i,val in enumerate(validresults):
			self.emit[i] = val.scanfit.fitresults.emitn

		ax=self.ui.dataset_mpl.ax
		ax.clear()
		ax.plot(self.emit)
		ax.figure.canvas.draw()

	def updateResults(self,val):
		ind = self.ui.imagenum_slider.value-1
		self.validimg[ind] = np.bool(val)

	def updateROI(self,rect):
		img=self.oimg[xstart:xstop,ystart:ystop]

