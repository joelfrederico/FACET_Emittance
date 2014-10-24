#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5
import numpy as np
import ButterflyEmittancePython as bt
import matplotlib.pyplot as plt
import matplotlib as mpl
from E200_get_data_cam import E200_get_data_cam

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

	camname_list = E200_get_data_cam(scalars)

	for camname in camname_list:
		head_str = 'ss_{}_'.format(camname)


	
		energy_axis_str = vectors['{}energy_axis'.format(head_str)]
		uids            = energy_axis_str['UID'].value

		for uid in uids:
	
			energy_axis          = mt.E200.E200_api_getdat(energy_axis_str,uid).dat[0][0]

			variance_str         = vectors['{}variance'.format(head_str)]
			variance             = mt.E200.E200_api_getdat(variance_str,uid).dat[0][0]

			LLS_beta_str         = vectors['{}LLS_beta'.format(head_str)]
			LLS_beta             = mt.E200.E200_api_getdat(LLS_beta_str,uid).dat[0][0]

			LLS_X_unweighted_str = arrays['{}LLS_X_unweighted'.format(head_str)]
			LLS_X_unweighted     = mt.E200.E200_api_getdat(LLS_X_unweighted_str,uid).dat[0][0]

			LLS_y_error_str      = vectors['{}LLS_y_error'.format(head_str)]
			LLS_y_error          = mt.E200.E200_api_getdat(LLS_y_error_str,uid).dat[0][0]

			image_str            = arrays['{}image'.format(head_str)]
			image                = mt.E200.E200_api_getdat(image_str,uid).dat[0][0]

			rect_str             = vectors['{}rect'.format(head_str)]
			rect                 = mt.E200.E200_api_getdat(rect_str,uid).dat[0][0]

			emit_n_str           = scalars['{}emit_n'.format(head_str)]
			emit_n               = mt.E200.E200_api_getdat(emit_n_str,uid).dat[0][0]

			betastar_str         = scalars['{}betastar'.format(head_str)]
			betastar             = mt.E200.E200_api_getdat(betastar_str,uid).dat[0][0]

			sstar_str            = scalars['{}sstar'.format(head_str)]
			sstar                = mt.E200.E200_api_getdat(sstar_str,uid).dat[0][0]

			quadval_str          = data.read_file['data']['raw']['scalars']['step_value']
			quadval              = mt.E200.E200_api_getdat(quadval_str,uid).dat[0]
		
			# ======================================
			# Fit figure
			# ======================================
			fig = plt.figure()
			ax = fig.add_subplot(1,1,1)
			bt.plotfit(
					x     = energy_axis      ,
					y     = variance         ,
					beta  = LLS_beta         ,
					X     = LLS_X_unweighted ,
					error = LLS_y_error      ,
					axes  = ax
					)
		
			filename = '{uid:0.0f}/{head_str}min_set_{setnumber}_UID_{uid:0.0f}'.format(setnumber=setnumber,uid=uid,head_str=head_str)
			mt.graphics.savefig(filename,fig=fig)
		
			# plt.close(fig)
			
			# ======================================
			# Image with ROI
			# ======================================
			fig = plt.figure()
			ax = fig.add_subplot(1,1,1)
			ax.imshow(image)
		
			# Get roi stuff
			rect_xy = rect[0:2]
			height  = rect[2]
			width   = rect[3]
		
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
		
			filename = '{uid:0.0f}/{head_str}image_set_{setnumber}_UID_{uid:0.0f}'.format(uid=uid,setnumber=setnumber,head_str=head_str)
			mt.graphics.savefig(filename,fig=fig,ext='jpg',dpi=300)
		
			# plt.close(fig)
		
			# ======================================
			# Make Dataset table of values
			# ======================================
			# env_curly=r'''llllllll'''
#                         table_begin = r'''
# \toprule
# \multicolumn{3}{c}{Dataset Info} & & \multicolumn{4}{c}{Fit Info} \\
# \cmidrule(l){1-3} \cmidrule(l){5-8}
#  Date                 & Dataset & UID && Pinch Energy & Normalized Emittance & Beta* [m] & S* [m] \\
#                       &         &     && [GeV]        & [mm-mrad]            &           & \\
# \midrule'''
			env_curly=r'''llll'''
			table_begin = r'''
\toprule
\multicolumn{4}{c}{Dataset Info} \\
\cmidrule(){1-4}
 Date                 & Dataset & UID & Quad Imaging Offset [GeV]\\
\midrule'''
			table_end= r'''
\bottomrule
'''
			table_mid = r'''
{}                  & {}      & {:0.0f} & {:0.3f} \\
'''
			
			# Calculate pinch energy
			size = np.dot(LLS_X_unweighted,LLS_beta)
			argmin = np.argmin(size)
			pinch_energy = energy_axis[argmin]
		
			# Add values to table_mid
			table_mid = table_mid.format(setdate,setnumber,uid,quadval)
		
			tablestr=''.join([table_begin,table_mid,table_end])
			
			filename = 'figs/{uid:0.0f}/{head_str}table_dataset_{setnumber}_UID_{uid:0.0f}.pdf'.format(head_str=head_str,uid=uid,setnumber=setnumber)
		
			mt.graphics.latexfig(tablestr,filename=filename,environment='tabular',env_curly=env_curly)

			# ======================================
			# Make Fit info table of values
			# ======================================
			env_curly=r'''lllll'''
			table_begin = r'''
\toprule
UID & \multicolumn{4}{c}{Fit Info} \\
\cmidrule(){2-5}
 & Pinch Energy & Normalized Emittance & Beta* [m] & S* [m] \\
 & [GeV]        & [mm-mrad]            &           & \\
\midrule'''
			table_end= r'''
\bottomrule
'''
			table_mid = r'''
{:0.0f} & {:0.3f} & {:0.3f} & {:0.3f} & {:0.3f}\\
'''
			
			# Calculate pinch energy
			size = np.dot(LLS_X_unweighted,LLS_beta)
			argmin = np.argmin(size)
			pinch_energy = energy_axis[argmin]
		
			# Add values to table_mid
			table_mid = table_mid.format(uid,pinch_energy,emit_n*1e6,betastar,sstar)
		
			tablestr=''.join([table_begin,table_mid,table_end])
			
			filename = 'figs/{uid:0.0f}/{head_str}table_fitinfo_{setnumber}_UID_{uid:0.0f}.pdf'.format(head_str=head_str,uid=uid,setnumber=setnumber)
		
			mt.graphics.latexfig(tablestr,filename=filename,environment='tabular',env_curly=env_curly)
			# data.close()
