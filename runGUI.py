#!/usr/bin/env python

import mytools as mt
from ButterflyGUI import ButterflyGUI
from analyze_matlab import analyze_matlab
import h5py as h5

infile = 'forpython.mat'
f=h5.File(infile)

app = mt.qt.get_app()
window = ButterflyGUI(analyze_matlab,f)
window.show()
app.exec_()
