import ButterflyEmittancePython as bt
import mytools.E200 as E200
import scipy.optimize as spopt
import mytools.slactrac as sltr

def find_QS_energy_ELANEX(E):
	def meritfunc(vec):
		E0=20.35
		twiss = sltr.Twiss(beta=0.5,
			   alpha=0
			   )
		# Get beamline
		beamline=bt.beamlines.IP_to_lanex_nobend(twiss,twiss)
		beamline.gamma = beamline.gamma * (E+E0)/E0
		# if E < 0:
		#         print 'E is {}, Gamma is {}'.format(E,beamline.gamma)
	
		# Change quads
		qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
		qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)
		
		beamline.elements[1].K1 = qs1_k_half
		beamline.elements[2].K1 = qs1_k_half
		beamline.elements[4].K1 = qs2_k_half
		beamline.elements[5].K1 = qs2_k_half
		
		r12 = beamline.R[0,1]
		r34 = beamline.R[2,3]

		return r12**2 + r34**2

	res = spopt.minimize(meritfunc,[200,-100],tol=1e-50)
	return res.x

def find_QS_relaxed(E):
	def meritfunc(vec):
		# This is the default energy for beamlines.
		E0=20.35
		# Energy interval to do optimization on
		E_bandwidth = 1.0

		# Starting emittance
		emit_x = 100e-6
		emit_y = 10e-6

		# Starting twiss
		twiss_x = sltr.Twiss(beta=0.5,
			   alpha=0
			   )
		twiss_y = sltr.Twiss(beta=5,
			   alpha=0
			   )
		beamline=bt.beamlines.IP_to_lanex_nobend(twiss_x,twiss_y)
		
		gamma_E0 = beamline.gamma
		beamline.gamma = gamma_E0 * (E+E0)/E0

		# Get default spot sizes
		sx0 = beamline.spotsize_x_end(emit_x)
		sy0 = beamline.spotsize_y_end(emit_y)

		# Change quads per input vector
		qs1_k_half = E200.setQS.bdes2K1(vec[0],E0)
		qs2_k_half = E200.setQS.bdes2K1(vec[1],E0)
		beamline.elements[1].K1 = qs1_k_half
		beamline.elements[2].K1 = qs1_k_half
		beamline.elements[4].K1 = qs2_k_half
		beamline.elements[5].K1 = qs2_k_half

		# Get spot size at default energy
		sx1 = beamline.spotsize_x_end(emit_x)
		sy1 = beamline.spotsize_y_end(emit_y)

		# Get spot size at other energy
		beamline.gamma = gamma_E0 * (E+E0+E_bandwidth)/E0
		sx2 = beamline.spotsize_x_end(emit_x)

		# return (sx2/sx1)**2 + (sx1/sx0)**2 + (sy1/sy0)**2
		return (sx1/sx0)**2 + (sy1/sy0)**2

	res = spopt.minimize(meritfunc,[200,-100],tol=1e-50)
	return res.x
