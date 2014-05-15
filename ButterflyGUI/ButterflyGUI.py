#!/usr/bin/env python

import sys
from PyQt4 import QtGui,QtCore
import mainwindow_auto as mw
import numpy as np

class ButterflyGUI(mw.Ui_MainWindow):
    def __init__(self, parent=None, name=None, fl=0):
        mw.__init__(self,parent,name,fl)

app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()
ui = mw.Ui_MainWindow()
ui.setupUi(window)
x=np.linspace(-3,3,100)
y=np.cos(x)
mw.MplWidget.MplCanvas.plot(x,y)
window.show()
# sys.exit(app.exec_())
