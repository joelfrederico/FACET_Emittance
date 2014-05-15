#!/usr/bin/env python

import mytools as mt
import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np

# class ButterflyGUI(mw.Ui_MainWindow):
#     def __init__(self, parent=None, name=None, fl=0):
#         mw.__init__(self,parent,name,fl)

# app = QtGui.QApplication(sys.argv)
app = mt.qt.get_app()
window = QtGui.QMainWindow()
ui = mw.Ui_MainWindow()
ui.setupUi(window)
# x=np.linspace(-3,3,100)
# y=np.cos(x)
# ui.imageview_mpl.ax.plot(x,y)
window.show()
app.exec_()
