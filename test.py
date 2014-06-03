#!/usr/bin/env python
import mytools as mt
import numpy as np

import ButterflyEmittancePython as bt
import mytools.E200 as E200
import scipy.optimize as spopt
import mytools.slactrac as sltr
from find_QS_energy_ELANEX import *

E0=20.35
emit_nx = 100e-6
emit_ny = 10e-6

this=find_QS_energy_ELANEX(0)
print this
vec=this.x
twiss_x = sltr.Twiss(beta=0.5,
	   alpha=0
	   )
twiss_y = sltr.Twiss(beta=5.0,
	   alpha=0
	   )
qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)

beamline=bt.beamlines.IP_to_lanex_nobend(twiss_x=twiss_x,twiss_y=twiss_y)
beamline.elements[1].K1 = qs1_k_half
beamline.elements[2].K1 = qs1_k_half
beamline.elements[4].K1 = qs2_k_half
beamline.elements[5].K1 = qs2_k_half
print '-----------------------'
print beamline.R[0,1]
print beamline.R[2,3]
print '-----------------------'

this=find_QS_relaxed(0)
print this
vec=this.x

qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)

beamline=bt.beamlines.IP_to_lanex_nobend(twiss_x=twiss_x,twiss_y=twiss_y)
beamline.elements[1].K1 = qs1_k_half
beamline.elements[2].K1 = qs1_k_half
beamline.elements[4].K1 = qs2_k_half
beamline.elements[5].K1 = qs2_k_half
print beamline.R

# =========================
# Analyze the optics
# =========================

# Peak resolution

print beamline.spotsize_y_end(emit=emit_ny/beamline.gamma)

