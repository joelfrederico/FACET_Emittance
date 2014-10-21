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

sets      = ['20140625','13438']
setdate   = sets[0]
setnumber = sets[1]

loadfile = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
data = mt.E200.E200_load_data(loadfile)

wf           = data.write_file
processed_wf = wf['data']['processed']
scalars_wf   = processed_wf['scalars']
vectors_wf   = processed_wf['vectors']
arrays_wf    = processed_wf['arrays']

rf         = data.read_file
raw_rf     = rf['data']['raw']
scalars_rf = raw_rf['scalars']
vectors_rf = raw_rf['vectors']
arrays_rf  = raw_rf['arrays']

# results = E200_get_data_cam(scalars)
# print results

camname = 'ELANEX'
head_str = 'ss_{}_'.format(camname)
energy_axis_str = vectors_wf['{}energy_axis'.format(head_str)]
uids            = energy_axis_str['UID'].value
uid = uids[0]

print type(uid)

elanex_str = raw_rf['images']['ELANEX']
# uid        = elanex_str['UID'][0][0]
elanex     = mt.E200.E200_api_getdat(elanex_str,uid)

quadval_str = data.read_file['data']['raw']['scalars']['step_value']

for val in quadval_str['UID'].value:
	if val == uid:
		print 'here'
	else:
		pass
		print 'nothere'


# quadval     = mt.E200.E200_api_getdat(quadval_str,uid).dat[0]
