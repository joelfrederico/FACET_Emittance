#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import mytools.slactrac as sltr
from find_QS_energy_ELANEX import *  # noqa
import copy

plt.close('all')


# =====================================
# Create slice-correlated data
# =====================================
# Get beamline
E0       = 20.35
delE     = 2.5
npts     = 101
en_array = np.linspace(E0-delE, E0+50*delE, npts)
# Constant of proportionality in normalized units of emittance. Usual emittance is 10mm-mrad
e0 = 10e-6
k  = 0.0
emit_array = (k*e0/delE) * (en_array - E0) + e0

beamline0      = find_QS_energy_ELANEX(E0)
beamline_array = np.array([])
for i, value in enumerate(en_array):
    beamline        = copy.deepcopy(beamline0)
    beamline.gamma  = sltr.GeV2gamma(value)
    beam_x          = sltr.BeamParams(beta=0.5, alpha=0, emit=e0/sltr.GeV2gamma(E0))
    beam_y          = sltr.BeamParams(beta=5.0, alpha=0, emit=e0/sltr.GeV2gamma(E0))
    beamline.beam_x = beam_x
    beamline.beam_y = beam_y
    beamline_array  = np.append(beamline_array, copy.deepcopy(beamline))

# =====================================
# Return spot sizes after everything
# =====================================
sigx = np.array([])
for i, value in enumerate(beamline_array):
    # sigx = np.append(sigx, value.beam_x.spotsize)
    sigx = np.append(sigx, value.spotsize_x_end)

plt.plot(en_array, sigx*1e6)
    
fontsize = 22

figpath = '/Users/joelfrederico/AAC2014/figs'

linewidth = 2

# ======================================
# Fit beamline scan
# ======================================
# scanresults = bt.fitBeamlineScan(beamline_array,
#                 variance,
#                 emitx,
#                 error=used_error,
#                 verbose=True,
#                 plot=False,
#                 eaxis=eaxis
#                 )

# =====================================
# Plot Fit
# =====================================
# figlabel='Butterfly Fit'
# ax0 = bt.plotfit(eaxis,
#                 variance,
#                 scanresults.fitresults.beta,
#                 scanresults.fitresults.X_unweighted,
#                 top       = 'Emittance and Beam Parameter Fit\nto Ionization-Injected Witness Bunch',
#                 figlabel  = figlabel,
#                 # figpath = figpath,
#                 bottom    = 'Energy [GeV]',
#                 # axes    = plotaxes,
#                 error     = used_error,
#                 linewidth = linewidth
#                 )

# mt.graphics.less_labels(ax0, y_fraction=1)
# mt.graphics.axesfontsize(ax0, fontsize)
# ax0.get_figure().tight_layout()

# mt.graphics.savefig(filename=figlabel, path=figpath)
