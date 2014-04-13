#!/usr/bin/env python
import mytools as mt
import mytools.E200.setQS as setQS
import sdds
import numpy as np
import sddsToolkit as st

import subprocess as sp
import shlex
import os.path
import time

# ======================================
# Vary energy from -0.6 to 0.4 GeV.
# ======================================
steps=6
en = np.linspace(-6,4,steps)/10

# ======================================
# Get K1 values for quads
# ======================================
qs1=np.zeros(steps)
qs2=np.zeros(steps)
for i,val in enumerate(en):
	qs1[i],qs2[i] = setQS.set_QS_energy_ELANEX(val)
	qs1[i] = setQS.bdes2K1(qs1[i],20.35)
	qs2[i] = setQS.bdes2K1(qs2[i],20.35)
	
# ======================================
# Write parameter scan file
# ======================================
# Open SDDS class
sddspar = sdds.SDDS(0)

# Write QS1 column
sddspar.defineSimpleColumn('QS1',sddspar.SDDS_DOUBLE)
sddspar.setColumnValueList('QS1',qs1.tolist(),page=1)

# Write QS2 column
sddspar.defineSimpleColumn('QS2',sddspar.SDDS_DOUBLE)
sddspar.setColumnValueList('QS2',qs2.tolist(),page=1)

# Save to scan.par
sddspar.save('scan.par')

# Wait for file.
while not os.path.isfile('scan.par'):
	time.sleep(0.1)

# ======================================
# Run elegant
# ======================================
# command = 'elegant drift.ele'
# sp.call(shlex.split(command))

def findcent(edge):
	delt=edge[1]-edge[0]
	return edge[0:-1]+delt

# ======================================
# Process pages into image
# ======================================
bins=100
imgs=np.zeros((6,bins,bins))
xedge=np.zeros((6,bins+1))
yedge=np.zeros((6,bins+1))
xcent=np.zeros((6,bins))
ycent=np.zeros((6,bins))
for i,val in enumerate(np.linspace(1,6,6)):
	page = st.loadpage('drift.out',i+1)
	x=st.sdds2array(page,'x')
	y=st.sdds2array(page,'y')
	d=st.sdds2array(page,'d')
	# imgs[i,:,:],extent[i,:]=mt.hist2d(x,y,labels=('Config Space','x','y'),bins=bins)
	imgs[i,:,:],xedge[i,:],yedge[i,:]=np.histogram2d(x,y,bins=bins)
	xcent[i]=findcent(xedge[i])
	ycent[i]=findcent(yedge[i])
