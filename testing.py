#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5

# app = myqt.get_app()
# buttons=[myqt.Button(QtGui.QMessageBox.Ok),myqt.Button('this',QtGui.QMessageBox.HelpRole,buttontype='Default')]
# # buttons=None
# buttonbox=myqt.ButtonMsg('this','that',buttons=buttons)
# 
# print buttonbox.clickedArray()

# data = mt.E200.E200_load_data('/nas/nas-li20-pm00/E200/2014/20140629/E200_13537/E200_13537.mat')
data = mt.E200.Filename('nas/nas-li20-pm00/E200/2014/20140629/E200_13537/E200_13537.mat')


print data.dir_beg
print data.dir_mid
print data.filename
print data.data_source_type
