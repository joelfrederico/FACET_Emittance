#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5
import numpy as np

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

data = mt.E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140625/E200_13438')
# data = mt.E200.Data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537/E200_13537.mat')
# data = mt.E200.Filename('nas/nas-li20-pm00/E200/2014/20140629/E200_13537/E200_13537.mat')

wf = data.write_file
vectors=wf['data']['processed']['vectors']

# val = [50,50]
# uid=1
# mt.E200.E200_api_updateUID(vectors,val,uid)

# print '==========================='

# newval = [10,20]
# newuid = 2

# mt.E200.E200_api_updateUID(vectors,newval,newuid)

# print '==========================='

# newval = [1,2]
# newuid = 3

# mt.E200.E200_api_updateUID(vectors,newval,newuid)

# print '==========================='

# out = mt.E200.E200_api_getdat(vectors,uids=[3,1])
# print out.dat
# print out.uid
