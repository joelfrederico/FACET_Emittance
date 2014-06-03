#!/usr/bin/env python
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import mytools as mt
from ButterflyGUI import ButterflyGUI
from analyze_matlab import analyze_matlab
import h5py as h5
import matplotlib as mpl
mpl.rcParams['image.aspect'] = 'auto'
import numpy as np

infile = 'forpython.mat'
f=h5.File(infile)

app = mt.qt.get_app()
window = ButterflyGUI(analyze_matlab,f)
# img = np.random.randn(10,10)
# window = ButterflyGUI(analyze_matlab,image=img)
# window.ui.imageview_mpl.img.image=img
window.show()
app.exec_()

