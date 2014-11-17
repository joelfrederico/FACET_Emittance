#!/usr/bin/env python -m pdb

import ButterflyEmittancePython as bt
import E200
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np
from E200_get_data_cam import E200_get_data_cam
from PyQt4 import QtGui,QtCore
import logging

# try:
#         wf.close()
# except:
#         pass

sets = [['20140625','13438'],
	# ['20140625','13449'],
	['20140629','13537'],
	['20140625','13450']]
# sets = [['20140625','13438'],
# sets = [['20140629','13537']]
# sets = [['20140625','13450']]

# ======================================
# Set up logging
# ======================================
logger = mt.mylogger(filename='postproc')

logger.critical('Logging set up')

for pair in sets:
	setdate=pair[0]
	setnumber=pair[1]

	loadfile = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
	
	data      = E200.E200_load_data(loadfile)
	wf        = data.write_file
	processed = wf['data']['processed']
	vectors   = processed['vectors']
	arrays    = processed['arrays']
	scalars   = processed['scalars']

	# camname_list = E200_get_data_cam(scalars)
	camnames = E200.E200_api_getdat(arrays['ss_camname'])
	camnamelist = np.unique(camnames.dat)

	for camname in camnamelist:
		# camname = 'CMOS_FAR'
		head_str = 'ss_{}_'.format(camname)
	
		energy_axis_str = vectors['{}energy_axis'.format(head_str)]
		uids            = energy_axis_str['UID'].value

		for uid in uids:
			logger.info('UID is: {}'.format(uid))
	
			energy_axis          = E200.E200_api_getdat(energy_axis_str,uid).dat[0]

			# ======================================
			# Scalars
			# ======================================

			emit_n_str           = scalars['{}emit_n'.format(head_str)]
			emit_n               = E200.E200_api_getdat(emit_n_str,uid).dat[0]

			betastar_str         = scalars['{}betastar'.format(head_str)]
			betastar             = E200.E200_api_getdat(betastar_str,uid).dat[0]

			sstar_str            = scalars['{}sstar'.format(head_str)]
			sstar                = E200.E200_api_getdat(sstar_str,uid).dat[0]

			img_max_str          = scalars['{}img_max'.format(head_str)]
			img_max              = E200.E200_api_getdat(img_max_str,uid).dat[0]

			# ======================================
			# Vectors
			# ======================================

			variance_str         = vectors['{}variance'.format(head_str)]
			variance             = E200.E200_api_getdat(variance_str,uid).dat[0]

			LLS_beta_str         = vectors['{}LLS_beta'.format(head_str)]
			LLS_beta             = E200.E200_api_getdat(LLS_beta_str,uid).dat[0]

			LLS_y_error_str      = vectors['{}LLS_y_error'.format(head_str)]
			LLS_y_error          = E200.E200_api_getdat(LLS_y_error_str,uid).dat[0]

			rect_str             = vectors['{}rect'.format(head_str)]
			rect                 = E200.E200_api_getdat(rect_str,uid).dat[0]


			# ======================================
			# Arrays
			# ======================================

			LLS_X_unweighted_str = arrays['{}LLS_X_unweighted'.format(head_str)]
			LLS_X_unweighted     = E200.E200_api_getdat(LLS_X_unweighted_str,uid).dat[0]

			image_str            = arrays['{}image'.format(head_str)]
			image                = E200.E200_api_getdat(image_str,uid).dat[0]

			quadval_str          = data.read_file['data']['raw']['scalars']['step_value']
			quadval              = E200.E200_api_getdat(quadval_str,uid).dat[0]
		
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
		
			filename = '{camname}/{uid:0.0f}/{head_str}min_set_{setnumber}_UID_{uid:0.0f}'.format(camname=camname,setnumber=setnumber,uid=uid,head_str=head_str)
			mt.graphics.savefig(filename,fig=fig)
		
			# plt.close(fig)
			
			# ======================================
			# Image with ROI
			# ======================================
			fig = plt.figure()
			ax = fig.add_subplot(1,1,1)
			im=ax.imshow(image,vmin=0,vmax=img_max)
		
			# Get roi stuff
			rect_xy = rect[0:2]
			width   = rect[2]
			height  = rect[3]
		
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

			plt.colorbar(mappable=im,ax=ax)
		
			fig.tight_layout()
		
			filename = '{camname}/{uid:0.0f}/{head_str}image_set_{setnumber}_UID_{uid:0.0f}'.format(camname=camname,uid=uid,setnumber=setnumber,head_str=head_str)
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
			
			filename = 'figs/{camname}/{uid:0.0f}/{head_str}table_dataset_{setnumber}_UID_{uid:0.0f}.pdf'.format(camname=camname,head_str=head_str,uid=uid,setnumber=setnumber)
		
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
			
			filename = 'figs/{camname}/{uid:0.0f}/{head_str}table_fitinfo_{setnumber}_UID_{uid:0.0f}.pdf'.format(camname=camname,head_str=head_str,uid=uid,setnumber=setnumber)
		
			mt.graphics.latexfig(tablestr,filename=filename,environment='tabular',env_curly=env_curly)
			# data.close()
