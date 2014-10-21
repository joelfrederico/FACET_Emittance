#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5
import numpy as np
import ButterflyEmittancePython as bt
import matplotlib.pyplot as plt
import matplotlib as mpl

try:
	wf.close()
except:
	pass

sets      = ['20140625','13438']
setdate   = sets[0]
setnumber = sets[1]

wf = h5.File('temp.hdf5','w')

# arrays = mt.E200.E200_create_data(wf,'test')


