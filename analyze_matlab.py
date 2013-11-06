#!/usr/bin/env python

import argparse
import numpy as np
import scipy.io as sio
import ButterflyEmittancePython as bt
import mytools.slactrac as sltr
import matplotlib.pyplot as plt
import mytools as mt
import copy

def analyze(infile):
	# Load and transfer matlab variables
	matvars        = sio.loadmat(infile)
	processed_data = matvars['processed_data']
	img_sub        = matvars['img_sub']
	hist_data      = matvars['hist_data']
	B5D36_en       = matvars['B5D36']

	sum_x     = processed_data['sum_x'][0,0]
	sum_y     = processed_data['sum_y'][0,0]
	x_meter   = processed_data['x_meter'][0,0]
	B5D36_en  = B5D36_en.item(0)
	new_en    = (B5D36_en-4.3)
	gamma     = (B5D36_en/0.5109989)*1e3
	new_gamma = (new_en/0.5109989)*1e3

	# Translate into script params
	davg         = (hist_data[:,0]/16.05-1)
	variance_old = hist_data[:,1]
	filt         = np.logical_not( (davg>(0.9971-1)) & (davg < (1.003-1)))
	filt         = np.logical_or(filt, np.logical_not(filt))

	# variance_old = variance
	
	num_pts = len(sum_x)
	variance  = np.zeros(num_pts)
	stddev    = np.zeros(num_pts)
	varerr    = np.zeros(num_pts)
	chisq_red = np.zeros(num_pts)
	for i,el in enumerate(sum_x):
		y                   = sum_x[i,:]
		popt,pcov,chisq_red[i] = mt.gaussfit(x_meter,y,sigma_y=np.sqrt(y),plot=False,variance_bool=True,verbose=False)
		variance[i]         = popt[2]
		varerr[i]           = pcov[2,2]
		stddev[i]           = np.sqrt(pcov[2,2])

	# Set up initial conditions
	# emitx = 100.1033e-6/40000 
	# betax = 59.69009e-3
	# alphax = -0.7705554

	# RMS
	# emitx = 0.00201/gamma
	# betax = 11.2988573693
	# alphax = 6.72697997971

	# Gauss fit
	emitx = 0.001363/gamma
	betax = 8.7
	alphax = 5.224
	gammax = (1+np.power(alphax,2))/betax
	twiss=np.array([betax,alphax,gammax])
	T = np.array([[betax,-alphax],[-alphax,gammax]])

	# Create Beamline {{{
	LIPOTR2TOR = sltr.Drift(length = 4.9266E+00)
	LTOR2QS1 = sltr.Drift(length = 0.5E+00)
	# QS1     : QUAD,L= 5.000000000E-01,K1= 3.077225846087095e-01,ORDER=2, DY=5.0e-30, DX=1.0e-30
	QS1 = sltr.Quad(length= 5.000000000E-01,K1= 3.077225846087095e-01)
	QS1._change_E(gamma,new_gamma)
	LQS12QS2 = sltr.Drift(length = 4.00E+00)
	# QS2     : QUAD,L= 5.000000000E-01,K1=-2.337527121004531e-01, ORDER=2
	QS2 = sltr.Quad(length= 5.000000000E-01,K1=-2.337527121004531e-01)
	QS2._change_E(gamma,new_gamma)
	LQS22BEND = sltr.Drift(length = 0.7428E+00)
	# B5D36_1 : CSBEN,L= 4.889500000E-01,          &
	#                ANGLE= 3.0E-03, 	     &
	#                EDGE1_EFFECTS=1,E1= 3.0E-3, &
	#                EDGE2_EFFECTS=0,    	     &
	#                HGAP= 3E-02, 		     &
	#                TILT= 1.570796327E+00, &
	#                SYNCH_RAD = 0
	#                
	# B5D36_2 : CSBEN,L= 4.88950000E-01,          &
	#                ANGLE= 3.0E-03, 	     &
	#                EDGE1_EFFECTS=0, 	     &
	#                EDGE2_EFFECTS=1,E2= 3.0E-3, &
	#                HGAP= 3E-02, 	    	     &
	#                TILT= 1.570796327E+00, &
	#                SYNCH_RAD = 0
	B5D36 = sltr.Bend(
			length= 2*4.889500000E-01,          
	               angle= 6.0E-03, 	     
		       order=1,
		       rotate=0
		       )
	               
	LBEND2TABLEv2 = sltr.Drift(length = 8.855E+00)
	LTABLE2WAFERv2 = sltr.Drift(length = 1.045E+00)
	
	beamline = sltr.Beamline(
			element_list=[
				LIPOTR2TOR    ,
				LTOR2QS1      ,
				QS1           ,
				QS1           ,
				LQS12QS2      ,
				QS2           ,
				QS2           ,
				LQS22BEND     ,
				B5D36       ,
				LBEND2TABLEv2 ,
				LTABLE2WAFERv2
				],
			gamma= gamma
			)

	beamline.calc_mat()
	beamline.change_energy(new_gamma);
	# for el in beamline.elements:
	#         print '---------------'
	#         print 'Energy of {} = {}'.format(el._type,el._gamma)
	#         try:
	#                 print 'K1 = {}'.format(el._K1)
	#         except:
	#                 pass
	#         try:
	#                 print 'K2 = {}'.format(el._K2)
	#         except:
	#                 pass
	#         try:
	#                 print 'Length = {}'.format(el._length)
	#         except:
	#                 pass
	# print '---------------'
	#}}}

	# Fit bowtie plot
	chisq_factor = 1
	# chisq_factor = 63.6632188
	used_error   = stddev*np.sqrt(chisq_factor)

	out          = bt.fitbowtie(beamline,davg,variance,filt,T,twiss,emitx,error=used_error, verbose=True)
	spotexpected = out.spotexpected
	X            = out.X
	beta         = out.beta
	covar        = out.covar
	# print covar

	figcher=plt.figure()
	top='Simulated Energy Emittance Measurement\nNOT PHYSICAL'
	bt.plotfit(filt,davg,variance,beta,out.X_unweighted,spotexpected,top,error=used_error)

	figchisquare = plt.figure()
	# plt.plot(davg,chisq_red)
	mt.plot_featured(davg,chisq_red,'.-',
			toplabel='Chi-Squared for Each Gaussian Fit',
			xlabel='$E/E_0$',
			ylabel='$\chi^2$')
	# print davg
	# print chisq_red

if __name__ == '__main__':

	parser=argparse.ArgumentParser(description=
			'Wrap python analysis to be called at the command line.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.2')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('-o','--output',action='store',
			help='Output filename. (Default: no file output.)')
	parser.add_argument('inputfile',
			help='Input Matlab v7 file.')
	parser.add_argument('-f','--fit', choices=['gauss', 'bigauss'], default='gauss', 
			help='Type of fit to spot size profile. (Default: %(default)s)')
	arg=parser.parse_args()

	out=analyze(arg.inputfile)
	
	if arg.verbose:
		plt.show()
