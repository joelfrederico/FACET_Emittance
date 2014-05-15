from PyQt4 import QtGui
import matplotlib as mpl
# import matplotlib.figure as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
	def __init__(self):
		self.fig=mpl.figure.Figure()
		self.ax=self.fig.add_subplot(111)
		FigureCanvas.__init__(self,self.fig)
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class MplWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.canvas=MplCanvas()
		self.vbl=QtGui.QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
