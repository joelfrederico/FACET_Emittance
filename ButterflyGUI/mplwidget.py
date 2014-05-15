import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
from PyQt4 import QtGui
import matplotlib as mpl
# import matplotlib.figure as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

# class MplCanvas(FigureCanvas):
# 	def __init__(self):
# 		self.fig=mpl.figure.Figure()
# 
# 		self.ax=self.fig.add_subplot(111)
# 		self.rect = mpl.patches.Rectangle((0,0),1,1)
# 		FigureCanvas.__init__(self,self.fig)
# 		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
# 		FigureCanvas.updateGeometry(self)

	#         self.fig.canvas.mpl_connect('figure_enter_event', self.enter_figure)

	# def enter_figure(self,event):
	#         print 'hello'

# class MplWidget(QtGui.QWidget):
# 	def __init__(self, parent=None):
# 		QtGui.QWidget.__init__(self,parent)
# 		self.canvas=MplCanvas()
# 		self.vbl=QtGui.QVBoxLayout()
# 		self.vbl.addWidget(self.canvas)
# 		self.setLayout(self.vbl)

class Mpl_Image(FigureCanvas):
	def __init__(self, parent=None):
		self.fig=mpl.figure.Figure()
		FigureCanvas.__init__(self,self.fig)
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.fig.canvas.mpl_connect('button_press_event', self.on_press)
		self.fig.canvas.mpl_connect('button_release_event', self.on_release)

		self.ax=self.fig.add_subplot(111)

		img = np.random.randn(10,10)
		self.rect = mpl.patches.Rectangle((-10,0),0,3,facecolor='w',edgecolor='r',alpha=0.5)

		self.ax.imshow(img)
		self.ax.add_patch(self.rect)

	def on_press(self,event):
		print 'press'
		self.x0 = event.xdata
		self.y0 = event.ydata

	def on_release(self,event):
		print 'release'
		self.x1 = event.xdata
		self.y1 = event.ydata
		self.rect.set_width(self.x1 - self.x0)
		self.rect.set_height(self.y1 - self.y0)
		self.rect.set_xy((self.x0, self.y0))
		self.ax.figure.canvas.draw()

class Mpl_Plot(Mpl_Image):
	pass
