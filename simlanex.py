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
import analyze_matlab as am

plt.close('all')

# ========================================
# Run elegant optimization
# ========================================
elefile = "drift.ele"
elepath = elefile[:string.find(elefile,'.ele')]
command = "elegant "
command = ''.join([command,' ',elefile])
# command = "elegant drift.ele"
print(command)
args = shlex.split(command)
# p = subprocess.Popen(args)
# p.wait()

print('Finished elegant.')

# ========================================
# Load particles from elegant
# ========================================
print('Loading...')
page = st.loadpage('drift.out')
# x = st.sdds2array(page,'x') * 1000
# y = st.sdds2array(page,'y') * 1000
x = st.sdds2array(page,'x')
y = st.sdds2array(page,'y')
d = st.sdds2array(page,'d')
print('Loaded!')

# ========================================
# Select only particles +/- 1% of center
# ========================================
bool = np.logical_and(d>-0.01,d<0.01)
x = x[bool]
y = y[bool]
d = d[bool]

# ========================================
# Create sum_x = array of spots to fit
# 	sum_x(i,:) = i-th histogram
#	representing slice of the beam.
# ========================================
top='This'
# mt.hist2d(y*1e3,(d+1),labels=[top,'y [mm]','$E/E_0$'],bins=res,fig=figdisp)
bins = [101,11]
h,extent = mt.hist2d(x,d,bins=bins)
h,xe,ye=np.histogram2d(x,d,bins=bins)
sum_x = np.transpose(h)

# ========================================
# Create x_meter = measurement of x-axis
# in meters
# ========================================
x_meter_del = xe[1]-xe[0]
x_meter = xe+x_meter_del
# Drop last element
x_meter = x_meter[0:-1]

# ========================================
# Fill in some easy values
# ========================================
qs1_k_half = 3.077225846087095e-01;
qs2_k_half = -2.337527121004531e-01;
B5D36_en   = 20.35
gamma      = (B5D36_en/0.5109989)*1e3

# ========================================
# Create davg = average delta for ea. slice
# ========================================
ye_del = ye[1]-ye[0]
davg = ye + ye_del
# Drop last element
davg = davg[0:-1]
plt.figure()
plt.plot(davg)

# plt.close('all')

am.analyze(sum_x,x_meter,qs1_k_half,qs2_k_half,gamma,davg)
plt.show()
