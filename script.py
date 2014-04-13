#!/usr/bin/env python
import sdds
import scipy as sp
import scipy.optimize as spopt
import numpy as np
import sddsToolkit as st
import mytools as mt
import matplotlib.pyplot as plt
import mytools.slactrac as sltr
import shlex, subprocess
import os, string
import ButterflyEmittancePython as bt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gs
import matplotlib as mpl
mpl.rcParams.update({'font.size':9})

plt.close('all')

# Run elegant optimization
elefile = "drift_opt.ele"
elepath = elefile[:string.find(elefile,'.ele')]
command = "elegant "
command = ''.join([command,' ',elefile])
# command = "elegant drift.ele"
print(command)
args = shlex.split(command)
p = subprocess.Popen(args)
p.wait()

print('Finished elegant.')

page = st.loadpage('drift.out')
# x = st.sdds2array(page,'x') * 1000
# y = st.sdds2array(page,'y') * 1000
x = st.sdds2array(page,'x')
y = st.sdds2array(page,'y')
d = st.sdds2array(page,'d')
res = 100

# Y Dispersion {{{
figdisp= plt.figure()
top='Dispersion at Measurement'
mt.hist2d(y*1e3,(d+1),labels=[top,'y [mm]','$E/E_0$'],bins=res,fig=figdisp)
# mt.graphics.savefig(top,elepath)
# plt.close(figdisp)
#}}}

# Simulated Energy Measurement {{{
figspec = plt.figure()
top='Simulated Energy Measurement\nNOT PHYSICAL'
mt.hist2d(x*1e6,(d+1),labels=[top,'x [$\mu$m]','$E/E_0$'],bins=res,fig=figspec)
# mt.graphics.savefig(top,elepath)
# plt.close(figspec)
#}}}

# Simulated Cherenkov Measurement {{{
figcher = plt.figure()
top='Simulated Cherenkov Measurement'
mt.hist2d(x*1e6,y*1e6,labels=[top,'x [$\mu$m]','y [$\mu$m]'],bins=res,fig=figcher)
# mt.graphics.savefig(top,elepath)
plt.close(figcher)
#}}}

# Simulation/Measurement

# Create Beamline {{{
DRIFT1 = sltr.Drift(length=5.8996)
DRIFT2 = sltr.Drift(length=4)
DRIFT3 = sltr.Drift(length=0.73182)
DRIFT4 = sltr.Drift(length=11.2901)

QS1 = sltr.Quad(
		length= 5.000000000E-01,
		K1= 2.959427141E-01 * 0.977
		)
QS2 = sltr.Quad(
		length= 5.000000000E-01,
		K1=-2.227412494E-01 * 0.977
		)

B5D36 = sltr.Bend(
		length=9.779000000E-01,
		angle=6.000000000E-03,
		order=1,
		rotate=0
		)

beamline = sltr.Beamline(
                element_list=[DRIFT1,QS1,QS1,DRIFT2,QS2,QS2,DRIFT3,B5D36,DRIFT4],
                gamma=40000
                )

beamline.calc_mat()
#}}}



# From sddsprocess results {{{
# emitx = 1.326446e-9
emitx = 100.1033e-6/40000 
betax = 59.69009e-3
alphax = -0.7705554
gammax = (1+np.power(alphax,2))/betax
twiss=np.array([betax,alphax,gammax])
T = np.array([[betax,-alphax],[-alphax,gammax]])

print 'Emittance is {}.'.format(emitx)
print 'Normalized emittance is {}.'.format(emitx*40000)
print 'Initial beta should be {}.'.format(betax)
print 'Initial alpha should be {}.'.format(alphax)
print 'Initial gamma should be {}.'.format(gammax)
print '------------------------------'
#}}}

# ==============================
# Run Cherenkov analysis {{{
# ==============================
out=bt.histcher(x,y,res)
[h,xval,davg] = out

stddevsq = bt.getstd(res,h,xval)

out = bt.fitbowtie(beamline,davg,stddevsq,T,twiss,emitx)
# [spotexpected,X,beta] = out
spotexpected = out.spotexpected
X            = out.X
beta         = out.beta
covar = out.covar

figcher=plt.figure()
top='Simulated Cherenkov Emittance Measurement'
bt.plotfit(davg,np.sqrt(stddevsq),beta,X,spotexpected,top,elepath)
plt.close(figcher)
#}}}

# ==============================
# Run energy analysis {{{
# ==============================
out = bt.histenergy(x,d,res)

[h,xval,davg] = out

stddevsq = bt.getstd(res,h,xval)

out = bt.fitbowtie(beamline,davg,stddevsq,T,twiss,emitx)
# [spotexpected,X,beta] = out
spotexpected = out.spotexpected
X            = out.X
beta         = out.beta
covar = out.covar

figenergy=plt.figure()
top='Simulated Energy Emittance Measurement\nNOT PHYSICAL'
bt.plotfit(davg,np.sqrt(stddevsq),beta,X,spotexpected,top,elepath)
# plt.close(figenergy)
#}}}

mt.graphics.tile()
