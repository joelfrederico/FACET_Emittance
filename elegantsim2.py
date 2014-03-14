#!/usr/bin/env python
import mytools as mt
import mytools.E200.setQS as setQS
import sdds
import numpy as np
import sddsToolkit as st
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gs

import subprocess as sp
import shlex
import os.path
import time

stepvalues = en
pxmin      = np.zeros(6)
ymin       = np.zeros(6)

# ======================================
# Set up PDF
# ======================================
# Create PDF
pp = PdfPages('output.pdf')
# Create figure
fig=mt.figure('Page 1',figsize=(8.5,11))
# Create larger gridspec
outergs= gs.GridSpec(4,2)
# pdb.set_trace()

# ======================================
# Find spot size for each step
# ======================================
# mt.figure('Shot')
for i,img in enumerate(imgs):
	# img=np.flipud(np.rot90(f[img[0]],3))
	img=np.rot90(img,1)
	ax=fig.add_subplot(outergs[i])
	ax.imshow(img,interpolation='none')
	fig.add_subplot(ax)

	# Fit individual slices
	print '========\nStepvalue = {}'.format(stepvalues[i])
	pxmin[i] = mt.findpinch(
			img,
			step=2,
			verbose=False)
	ymin[i] = pxmin[i]*(yedge[i,1]-yedge[i,0])

outergs.tight_layout(fig)

# ymin = pxmin*res_y*1e3

# out=np.polyfit(stepvalues/20.35,ymin,1)
out=np.polyfit(stepvalues/20.35,ymin,1)

fig2=mt.plot_featured(stepvalues,pxmin,'.-',stepvalues,np.polyval(out,stepvalues/20.35),'-',
		figlabel = 'Fit',
		toplabel='Dispersion Measurement: {}mm'.format(out[0]),
		xlabel = 'Energy offset [GeV]',
		ylabel = 'Pinch location (y) [mm]',
		legend= ('Data','Fit')
		)
plt.tight_layout()

# pp.savefig(fig)
pp.savefig(fig2)
pp.close()

plt.show()
