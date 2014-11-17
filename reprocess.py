#!/usr/bin/env python
#!/usr/bin/env python #-m pdb
#  import signal
#  signal.signal(signal.SIGINT, signal.SIG_DFL)

import pdb

import ButterflyEmittancePython as bt
import E200
import h5py as h5
import inspect
import matplotlib as mpl
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np
import analyze_matlab as analyze_matlab

from E200_get_data_cam import E200_get_data_cam
from PyQt4             import QtGui,QtCore
from analyze_matlab    import analyze_matlab
from save_analysis     import save_analysis

sets = [
		['20140625','13438'],
		['20140625','13449'],
		['20140625','13450'],
		['20140629','13537']
	]

#  sets = [['20140625','13438'],
#  sets = [['20140629','13537']]
#  sets = [['20140625','13450']]

logger = mt.mylogger(filename='reprocess')
logger.debug('Beginning reprocessing...')

for pair in sets:
	setdate=pair[0]
	setnumber=pair[1]

	loadfile     = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
	data         = E200.E200_load_data(loadfile)
	wf           = data.write_file
	data_wf      = wf['data']
	processed_wf = data_wf['processed']
	arrays_wf    = processed_wf['arrays']
	vectors_wf   = processed_wf['vectors']

	rf         = data.read_file
	data_rf    = rf['data']

	camname_list = E200.E200_api_getdat(arrays_wf['ss_camname'])
	camname_list_UID = np.array([camname_list.UID]).flatten()

	for i,uid in enumerate(camname_list_UID):
		camname  = camname_list.dat[i]
		head_str = 'ss_{}_'.format(camname)
		
		logger.debug('Loaded camname: {camname}, UID: {uid}'.format(camname=camname,uid=uid))

		oimg         = E200.E200_api_getdat(arrays_wf['{}image'.format(head_str)],uid)
		oimg         = oimg.dat[0]
		rect_vec_str = E200.E200_api_getdat(vectors_wf['{}rect'.format(head_str)],uid)
		rect_vec     = rect_vec_str.dat[0]
		
		rect = mt.qt.Rectangle(*rect_vec)

		logger.debug('Re-analyzing...')
		out = analyze_matlab(
			data     = data_rf ,
			camname  = camname ,
			oimg     = oimg    ,
			rect     = rect    ,
			uid      = uid
			)

		logger.debug('Re-saving...')
		save_analysis(
				dataset     = data     ,
				analyze_out = out      ,
				rect_arr    = rect_vec ,
				camname     = camname  ,
				oimg        = oimg     ,
				uid         = uid
				)

# if __name__ == '__main__':
# 	parser=argparse.ArgumentParser(description='Loads and runs a gui to analyze saved spectrometer data.')
# 	parser.add_argument('-v','--verbose',action='store_true',
# 			help='enable verbose mode')
# 	parser.add_argument('-l','--log',default='info',choices=['debug','info','warning','error','critical'],
# 			help='increase logging level')
# 	parser.add_argument('-f','--file',
# 			help='file to process')
# 	parser.add_argument('-c','--camera',
# 			help='camera name')
# 	parser.add_argument('-i','--imgnum',type=int,
# 			help='image number')
# 
# 	arg=parser.parse_args()
# 
# 	runGUI(arg.file,arg.camera,arg.imgnum,verbose=arg.verbose,loglevel=arg.log)
