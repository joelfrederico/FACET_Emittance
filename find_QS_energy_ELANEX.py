import ButterflyEmittancePython as bt
import mytools as mt
import mytools.E200 as E200
import scipy.optimize as spopt
import mytools.slactrac as sltr
import numpy as np
import copy

def setquads(beamline,vec):
	# qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
	# qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)
	vec = np.float64(vec)
	# print vec
	qs1_k_half = vec[0]
	qs2_k_half = vec[1]

	beamline.elements[3].K1 = qs1_k_half
	beamline.elements[4].K1 = qs1_k_half
	beamline.elements[6].K1 = qs2_k_half
	beamline.elements[7].K1 = qs2_k_half

	return beamline

def find_QS_energy(beamline,
		E):

	beamline0=copy.deepcopy(beamline)
	beamline0.gamma = sltr.GeV2gamma(E)

	def meritfunc(vec):
		# Set up variables
		vec = np.float64(vec)
		beamline = copy.deepcopy(beamline0)
	
		# Change quads
		beamline = setquads(beamline,vec)
		
		# Get r values
		r12 = beamline.R[0,1]
		r34 = beamline.R[2,3]

		# Merit value
		out = r12**2 + r34**2
		out = out * 1e2
		# print out
		return out

	guessKvec   = np.array([E200.setQS.bdes2K1(250,20.35),E200.setQS.bdes2K1(-150,20.35)])
	res         = spopt.minimize(meritfunc,guessKvec,tol=1e-5)
	beamlineout = setquads(beamline0,res.x)
	if res.success==False:
		print res
		raise RuntimeError('Optimization did not converge.')
	return beamlineout

def find_QS_energy_cherfar(E):
	E  = np.float64(E)
	E0 = np.float64(20.35)

	beam_x=sltr.BeamParams(beta=0.5,alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(E+E0))
	beam_y=sltr.BeamParams(beta=5.0,alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(E+E0))
	beamline0 = bt.beamlines.IP_to_cherfar(beam_x=beam_x,beam_y=beam_y)

	beamlineout = find_QS_energy(beamline0,E+E0)

	return beamlineout

def find_QS_energy_ELANEX(E):
	E  = np.float64(E)
	E0 = np.float64(20.35)

	beam_x=sltr.BeamParams(beta=0.5,alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(E+E0))
	beam_y=sltr.BeamParams(beta=5.0,alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(E+E0))
	beamline0 = bt.beamlines.IP_to_lanex(beam_x=beam_x,beam_y=beam_y)

	beamlineout = find_QS_energy(beamline0,E+E0)

	return beamlineout

def find_QS_relaxed(E):
	this=find_QS_energy_ELANEX(0)
	vec0=this.x
	def meritfunc(vec):
		# This is the default energy for beamlines.
		E0=20.35
		# Energy interval to do optimization on
		E_bandwidth = 1.0

		# Starting emittance
		emit_nx = np.float64(100e-6)
		emit_ny = np.float64(10e-6)

		# Starting BeamParams
		beam_x = sltr.BeamParams(beta=0.5,
			   alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(20.35)
			   )
		beam_y = sltr.BeamParams(beta=5,
			   alpha=0,emit_n=20e-6,gamma=sltr.GeV2gamma(20.35)
			   )
		beamline=bt.beamlines.IP_to_lanex_nobend(beam_x,beam_y)
		qs1_k_half = E200.setQS.bdes2K1(vec0[0],E0)
		qs2_k_half = E200.setQS.bdes2K1(vec0[1],E0)
		beamline.elements[1].K1 = qs1_k_half
		beamline.elements[2].K1 = qs1_k_half
		beamline.elements[4].K1 = qs2_k_half
		beamline.elements[5].K1 = qs2_k_half
		
		gamma_E0 = beamline.gamma
		beamline.gamma = gamma_E0 * (E+E0)/E0

		# Get default spot sizes
                # print beamline.R
		# sx0 = beamline.spotsize_x_end(emit_n=emit_nx)
		# sy0 = beamline.spotsize_y_end(emit_n=emit_ny)
		sx0 = beamline.spotsize_x_end(emit=emit_nx/beamline.gamma)
		sy0 = beamline.spotsize_y_end(emit=emit_ny/beamline.gamma)

		# Change quads per input vector
		qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
		qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)
		beamline.elements[1].K1 = qs1_k_half
		beamline.elements[2].K1 = qs1_k_half
		beamline.elements[4].K1 = qs2_k_half
		beamline.elements[5].K1 = qs2_k_half

		# Get spot size at default energy
		# sx1 = beamline.spotsize_x_end(emit_n=emit_nx)
		# sy1 = beamline.spotsize_y_end(emit_n=emit_ny)
		sx1 = beamline.spotsize_x_end(emit=emit_nx/beamline.gamma)
		sy1 = beamline.spotsize_y_end(emit=emit_ny/beamline.gamma)

		# Get spot size at other energy
		beamline.gamma = gamma_E0 * (E+E0+E_bandwidth)/E0
		# sx2 = beamline.spotsize_x_end(emit_n=emit_nx)
		sx2 = beamline.spotsize_x_end(emit=emit_nx/beamline.gamma)

		out=(sx2-sx1)**2 + (sx1-sx0)**2 + (sy1-sy0)**2
		# out=(sx1-sx0)**2 + (sy1-sy0)**2
		# print out
		# return out

		r12 = beamline.R[0,1] * 1000
		r34 = beamline.R[2,3] * 1000

		return r12**2 + r34**2

	res = spopt.minimize(meritfunc,[250,-150],tol=1e-50)
	return res
