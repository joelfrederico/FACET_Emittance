#!/usr/bin/env python

import pickle
import ButterflyEmittancePython as bt
import numpy as np
import matplotlib.pyplot as plt
import mytools as mt
from matplotlib import cm

plt.close('all')

f = open('oldmydata.pkl')
pjar = pickle.load(f)
f.close()

shot17 = pjar.fitresults[16]

fontsize=22

eaxis = shot17.scanfit.fitresults.eaxis
variance = shot17.scanfit.fitresults.y_unweighted
variance = np.reshape(variance,(variance.shape[0],))
used_error = shot17.scanfit.fitresults.y_error[:,0]
scanresults = shot17.scanfit

figpath = '/Users/joelfrederico/AAC2014/figs'

linewidth=2

# =====================================
# Plot Fit
# =====================================
figlabel='Butterfly Fit'
ax0 = bt.plotfit(eaxis,
		variance,
		scanresults.fitresults.beta,
		scanresults.fitresults.X_unweighted,
		top       = 'Emittance and Beam Parameter Fit\nto Ionization-Injected Witness Bunch',
		figlabel  = figlabel,
		# figpath = figpath,
		bottom    = 'Energy [GeV]',
		# axes    = plotaxes,
		error     = used_error,
		linewidth = linewidth
		)

mt.graphics.less_labels(ax0,y_fraction=1)
mt.graphics.axesfontsize(ax0,fontsize)
ax0.get_figure().tight_layout()

mt.graphics.savefig(filename=figlabel,path=figpath)

# =====================================
# Plot Image
# =====================================
fig = plt.figure()
ax  = fig.add_subplot(1,1,1)
# xx = mt.linspaceborders(div*1e3)
# yy = mt.linspaceborders(energy)
yy = mt.linspaceborders(shot17.oimgeaxis)
xx = mt.linspaceborders(mt.linspacestep(1,shot17.oimg.shape[0]))
yy = yy[shot17.ystart:shot17.ystop]
xx = xx[shot17.xstart:shot17.xstop]*shot17.res*1e6/np.sqrt(2)
xx = xx-np.mean(xx)
vmax = 1600
p1   = ax.pcolormesh(xx,yy,shot17.img.transpose(),vmax=vmax,cmap=cm.RdBu_r)
# p1   = ax.contourf(xx,yy,shot17.img.transpose(),vmax=1500,cmap=cm.Blues)
cbar = fig.colorbar(p1)
p2   = ax.contour(xx,yy,shot17.img.transpose(),levels=np.linspace(0,vmax,6),colors='Black',linewidths=linewidth)
ax.axhspan(ymin=yy[36*5],ymax=yy[37*5],color='Red',fill=False,linewidth=4)

ax.axis([xx.min(),xx.max(),yy.min(),yy.max()])
toplabel='Ionization-Injected Witness Profile at Lanex'
windowlabel='Lanex'
mt.addlabel(fig=fig,axes=ax,windowlabel=windowlabel,toplabel=toplabel,ylabel='Energy [GeV]',xlabel='Horizontal Axis $x$ [$\mu$m]',cb=cbar,clabel='Counts')


mt.graphics.less_labels(ax,x_fraction=1)
mt.graphics.axesfontsize(ax,fontsize)

fig.tight_layout()

mt.graphics.savefig(filename=toplabel,path=figpath)

# =====================================
# Plot Gauss
# =====================================
gfit = shot17.gaussfits[36]
fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)
gfit.plot(ax2,x_mult=1e6,linewidth=linewidth)

windowlabel='GaussFitShot37'
toplabel='Gaussian Fit to 37th Slice'
xlabel='Horizontal Axis $x$ [$\mu m$]'
ylabel = 'Counts'
mt.addlabel(fig=fig2,axes=ax2,windowlabel=windowlabel,toplabel=toplabel,ylabel=ylabel,xlabel=xlabel)

mt.graphics.less_labels(ax2,x_fraction=1)
mt.graphics.axesfontsize(ax2,fontsize)

fig2.tight_layout()

mt.graphics.savefig(filename=toplabel,path=figpath)

plt.show()
