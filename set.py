#!/usr/bin/env python

import pickle
# import ButterflyEmittancePython as bt
import numpy as np
import matplotlib.pyplot as plt
import mytools as mt
# from matplotlib import cm

plt.close('all')

f = open('newmydata.pkl')
pjar = pickle.load(f)
f.close()

figpath = '/Users/joelfrederico/AAC2014'

valid_bool = pjar.valid

analysis_arr = pjar.fitresults[valid_bool]

num_results = analysis_arr.shape[0]
emit_n      = np.zeros(num_results)
emit        = np.zeros(num_results)
beta        = np.zeros(num_results)
alpha       = np.zeros(num_results)
betastar    = np.zeros(num_results)
sstar       = np.zeros(num_results)
result      = mt.linspacestep(1, num_results)
for i, arr in enumerate(analysis_arr):
    emit_n[i]   = arr.scanfit.fitresults.emitn
    emit[i]     = arr.scanfit.fitresults.emit
    beta[i]     = arr.scanfit.fitresults.twiss.beta
    alpha[i]    = arr.scanfit.fitresults.twiss.alpha
    betastar[i] = arr.scanfit.fitresults.twiss.betastar
    sstar[i]    = arr.scanfit.fitresults.twiss.sstar

linewidth = 2

# =====================================
# Plot Emittance
# =====================================
y = emit_n*1e6

fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)
line = ax.plot(result, y, 'o-', linewidth=linewidth)

toplabel    = 'Ionization-Injected Witness Emittance'
windowlabel = toplabel
xlabel      = 'Result #'
ylabel      = 'Emittance [mm-mrad]'

mt.addlabel(fig=fig, axes=ax, windowlabel=windowlabel, toplabel=toplabel, xlabel=xlabel, ylabel=ylabel)

fig.tight_layout()

mt.graphics.savefig(filename=toplabel, path=figpath)

# =====================================
# Plot Spot size
# =====================================
y = np.sqrt(emit*betastar)*1e6

fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)
line = ax.plot(result, y, 'o-', linewidth=linewidth)

windowlabel = 'Spot Size'
toplabel    = 'Ionization-Injected Witness Spot Size\nNear Plasma Exit'
xlabel      = 'Result #'
ylabel      = 'Spot Size $\\sqrt{\\langle x^2 \\rangle }$ [$\\mu$m]'

mt.addlabel(fig=fig, axes=ax, windowlabel=windowlabel, toplabel=toplabel, xlabel=xlabel, ylabel=ylabel)

fig.tight_layout()

mt.graphics.savefig(filename=windowlabel, path=figpath)

# =====================================
# Plot Divergence
# =====================================
y = np.sqrt(emit*(1/betastar))*1e6

fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)
line = ax.plot(result, y, 'o-', linewidth=linewidth)

windowlabel = 'Divergence'
toplabel    = 'Ionization-Injected Witness Divergence\nNear Plasma Exit'
xlabel      = 'Result #'
ylabel      = 'Divergence $\\sqrt{\\langle {x\'}^2 \\rangle }$ [$\\mu$rad]'

mt.addlabel(fig=fig, axes=ax, windowlabel=windowlabel, toplabel=toplabel, xlabel=xlabel, ylabel=ylabel)

fig.tight_layout()

mt.graphics.savefig(filename=windowlabel, path=figpath)
