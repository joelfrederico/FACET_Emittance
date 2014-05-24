#!/usr/bin/env python

# My code
import mytools as mt
import mytools.E200 as E200
import mytools.slactrac as sltr
import sddsToolkit as st
import ButterflyEmittancePython as bt
from find_QS_energy_ELANEX import find_QS_energy_ELANEX
from derivative import derivative

# Support code
import sdds
import scipy.optimize as spopt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gs
import matplotlib as mpl
mpl.rcParams.update({'font.size':9})

# System code
import subprocess as sp
import shlex
import os.path
import time

plt.close('all')

# Create PDF
pp = PdfPages('output.pdf')
# Create figure
fig=mt.figure('Page 1',figsize=(8.5,11))

emass = 0.5109989e-3

twiss = sltr.Twiss(beta=0.5,
	   alpha=0
	   )

emit=50e-6

def imagedbeamline(Eimg):
	# Initialize beamline
	beamline=bt.beamlines.IP_to_lanex_nobend(twiss,twiss)
	# beamline.gamma = (1+E/20.35)*39824
	
	# bact = E200.setQS.set_QS_energy_ELANEX(Eimg-20.35)
	# bact = E200.setQS.set_QS_energy_ELANEX(0)
	bact = find_QS_energy_ELANEX(Eimg-20.35)
	# bact = find_QS_energy_ELANEX(0)
	qs1_k_half = E200.setQS.bdes2K1(bact[0],20.35)
	qs2_k_half = E200.setQS.bdes2K1(bact[1],20.35)

        gamma0 = beamline.gamma

	beamline.gamma = gamma0 * Eimg/20.35
	
	beamline.elements[1].K1 = qs1_k_half
	beamline.elements[2].K1 = qs1_k_half
	beamline.elements[4].K1 = qs2_k_half
	beamline.elements[5].K1 = qs2_k_half

        return beamline

def beamlinefromE(Eimg,Etest):
        beamline = imagedbeamline(Eimg)

        # beamline.gamma = Etest/20.35
        beamline.gamma = Etest/emass
	# print('R12 = {}, Analytic = {}, From Py = {}'.format(
	#         beamline.R[0,1],
	#         -beamline.R[0,0]*beamline.R[1,0]*0.5,
	#         beamline.twiss_x_end.alpha))
	# print '================================'
	# print beamline.twiss_x_end.alpha


	# print beamline.twiss_x_end.alpha
	return beamline

def alphafromE(Eimg,Etest):
	beamline = beamlinefromE(Eimg,Etest)
	return beamline.twiss_x_end.alpha

def betafromE(Eimg,Etest):
	beamline = beamlinefromE(Eimg,Etest)
	# print beamline.twiss_x_end.beta
	return beamline.twiss_x_end.beta

def dbeta_dE(Eimg,En):
        beamline = imagedbeamline(Eimg)
        beamline.gamma = En/emass
        def calcR11(E):
                beamline.gamma = E/emass
                return beamline.R[0,0]
        def calcR12(E):
                beamline.gamma = E/emass
                return beamline.R[0,1]

        R11 = beamline.R[0,0]
        R12 = beamline.R[0,1]
        R11p = derivative(calcR11,En)
        R12p = derivative(calcR12,En)

        print 'dbeta/dE = {}'.format(R11*twiss.beta**2*R11p + R12*R12p)
        
def dalpha_dE(Eimg,En):
        beamline = imagedbeamline(Eimg)
        beamline.gamma = En/emass
        def calcalpha(E):
                beamline.gamma = E/emass
                return beamline.twiss_x_end.alpha

        ap = derivative(calcalpha,En,tol=1e-6)

        print 'dalpha/dE = {}'.format(ap)

# numsteps = 101
numsteps = 11
width = 4
Escan = np.linspace(20.35-width,20.35+width,numsteps)
Eres = np.zeros(numsteps)
Eres2 = np.zeros(numsteps)
Eres3 = np.zeros(numsteps)
Eres4 = np.zeros(numsteps)

for i,val in enumerate(Escan):
	def minfunc(Etest):
		Etest=Etest[0]
                return betafromE(val,Etest)**2
                # return alphafromE(val,Etest)**2
	
	res = spopt.minimize(minfunc,val)
	Eres[i] = res.x[0]

	print('Result = {}'.format(np.sqrt(minfunc(res.x))))
        dbeta_dE(val,res.x[0])
        dalpha_dE(val,res.x[0])

for i,val in enumerate(Escan):
        beamline = imagedbeamline(val)
        def calcR11(E):
                beamline.gamma = E/emass
                return beamline.R[0,0]
        def calcR12(E):
                beamline.gamma = E/emass
                return beamline.R[0,1]

        R11 = beamline.R[0,0]
        R12 = beamline.R[0,1]
        R11p = derivative(calcR11,val)
        R12p = derivative(calcR12,val)

        Eres2[i] = val - (R11*R11p*twiss.beta**2+R12*R12p)/(R11p**2*twiss.beta**2 + R12p**2)
        print 'Energy should be {}'.format(Eres2[i])

fig=plt.figure()
plt.plot(Escan,Eres,'.-')
mt.addlabel('Pinch Energy Proportional to Imaging Energy','Image Energy','Pinch Energy')
pp.savefig(fig)
pp.close()

for i,val in enumerate(Escan):
        Eres3[i] = betafromE(20.35,val)
        Eres4[i] = alphafromE(20.35,val)

plt.figure()
plt.plot(Escan,Eres3,'.-')

plt.figure()
plt.plot(Escan,Eres4,'.-')

plt.tight_layout()
# plt.show()
