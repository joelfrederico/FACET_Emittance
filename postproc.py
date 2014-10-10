#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5
import numpy as np
import ButterflyEmittancePython as bt
import matplotlib.pyplot as plt
import matplotlib as mpl

# app = myqt.get_app()
# buttons=[myqt.Button(QtGui.QMessageBox.Ok),myqt.Button('this',QtGui.QMessageBox.HelpRole,buttontype='Default')]
# # buttons=None
# buttonbox=myqt.ButtonMsg('this','that',buttons=buttons)
# 
# print buttonbox.clickedArray()

try:
	wf.close()
except:
	pass

sets = [['20140625','13438']]

for pair in sets:
	setdate=pair[0]
	setnumber=pair[1]

	loadfile = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
	
	data      = mt.E200.E200_load_data(loadfile)
	wf        = data.write_file
	processed = wf['data']['processed']
	vectors   = processed['vectors']
	arrays    = processed['arrays']
	scalars   = processed['scalars']
	
	energy_axis_str = vectors['ss_energy_axis']
	uid             = energy_axis_str['UID'][()]
	uid             = uid[0]
	
	energy_axis          = mt.E200.E200_api_getdat(energy_axis_str,uid)

	variance_str         = vectors['ss_variance']
	variance             = mt.E200.E200_api_getdat(variance_str,uid)

	LLS_beta_str         = vectors['ss_LLS_beta']
	LLS_beta             = mt.E200.E200_api_getdat(LLS_beta_str,uid)

	LLS_X_unweighted_str = arrays['ss_LLS_X_unweighted']
	LLS_X_unweighted     = mt.E200.E200_api_getdat(LLS_X_unweighted_str,uid)

	LLS_y_error_str      = vectors['ss_LLS_y_error']
	LLS_y_error          = mt.E200.E200_api_getdat(LLS_y_error_str,uid)

	image_str            = arrays['ss_image']
	image                = mt.E200.E200_api_getdat(image_str,uid)

	rect_str             = arrays['ss_rect']
	rect                 = mt.E200.E200_api_getdat(rect_str,uid)

	ind = 0
	
	# ======================================
	# Fit figure
	# ======================================
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	bt.plotfit(
			x     = energy_axis.dat[ind]      ,
			y     = variance.dat[ind]         ,
			beta  = LLS_beta.dat[ind]         ,
			X     = LLS_X_unweighted.dat[ind] ,
			error = LLS_y_error.dat[ind]      ,
			axes  = ax
			)

	filename = 'SS_min_set_{}_UID_{:0.0f}'.format(setnumber,uid)
	mt.graphics.savefig(filename,fig=fig)

	# plt.close(fig)
	
	# ======================================
	# Image with ROI
	# ======================================
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.imshow(image.dat[ind])

	# Get roi stuff
	rect_xy = rect.dat[ind][0:2]
	height  = rect.dat[ind][2]
	width   = rect.dat[ind][3]

	p = mpl.patches.Rectangle(rect_xy,width,height,facecolor='w',edgecolor='r',alpha=0.5)

	# Add roi
	ax.add_patch(p)

	# Add axes
	mt.addlabel(
			toplabel='Image Fit Region',
			xlabel='Energy',
			ylabel='X',
			axes=ax
			)

	fig.tight_layout()

	filename = 'SS_image_set_{}_UID_{:0.0f}'.format(setnumber,uid)
	mt.graphics.savefig(filename,fig=fig,ext='jpg',dpi=300)

	# plt.close(fig)

	# ======================================
	# Make table of values
	# ======================================
	tablestr = 

	# data.close()
