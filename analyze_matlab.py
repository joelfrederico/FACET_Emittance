#!/usr/bin/env python
import argparse
import numpy as np
import scipy.io as sio
import ButterflyEmittancePython as bt
import mytools.slactrac as sltr
import matplotlib.pyplot as plt
import mytools as mt
import mytools.E200 as E200
import copy
import h5py as h5
import pdb as _pdb

plt.close('all')
def wrap_analyze(infile):
	# ======================================
	# Load and transfer matlab variables
	# ======================================
	f=h5.File(infile);
	data=f['data']
	
	# ======================================
	# Load an image
	# ======================================
	step_value=data['raw']['scalars']['step_value']
	zero_uids=mt.E200.E200_api_getUID(step_value,0,f)
	cegain = data['raw']['images']['CEGAIN']
	img_uids=cegain['UID'][:,0]
	# wantedUIDs=zero_uids[16]
	valid_img_uids=np.intersect1d(zero_uids,img_uids)
	wantedUIDs=valid_img_uids[1]
	wantedUIDs_bool=np.in1d(img_uids,wantedUIDs)
	imgs=cegain['dat'][:,0]
	img=imgs[wantedUIDs_bool]
	img=mt.E200.E200_load_images(img,f)
	# Show image loaded
	mt.figure('Image in')
	plt.imshow(img[0])

	# ======================================
	# Load Matlab-processed info
	# ======================================
	processed_data = f['processed_data']
	img_sub        = f['img_sub']
	hist_data      = f['hist_data']
	sum_x     = np.array(processed_data['sum_x'])
	sum_y     = np.array(processed_data['sum_y'])
	x_meter   = np.array(processed_data['x_meter'])

	# ======================================
	# Load quad values
	# ======================================
	step_uids=step_value['UID'][:,0]
	step_vals=E200.E200_api_getdat(step_value,wantedUIDs,f)
	bact = E200.setQS.set_QS_energy_ELANEX(step_vals[0])
	qs1_k_half = E200.setQS.bdes2K1(bact[0],20.35)
	qs2_k_half = E200.setQS.bdes2K1(bact[1],20.35)

	# ======================================
	# Load mag energy/gamma
	# ======================================
	B_spect = h5file[h5file['data']['raw']['scalars']['LI20_LGPS_3330_BDES']['dat'][0,0]][0,0]
	gamma     = (20.35/0.5109989)*1e3

	# ======================================
	# Translate into script params
	# ======================================
	quadE        = 20.35
	davg         = (hist_data[0,:]/quadE-1)
	variance_old = hist_data[1,:]

	# ======================================
	# Get spot sizes for strips
	# ======================================
	num_pts = sum_x.shape[1]
	variance  = np.zeros(num_pts)
	stddev    = np.zeros(num_pts)
	varerr    = np.zeros(num_pts)
	chisq_red = np.zeros(num_pts)
	for i in mt.linspacestep(0,num_pts-1):
		y                   = sum_x[:,i]
		y = np.abs(y)
		# print y
		erry = np.sqrt(y)
		erry[erry==0] = 0.3
		# plt.plot(y)
		# plt.show()
		# popt,pcov,chisq_red[i] = mt.gaussfit(x_meter,y,sigma_y=erry,plot=True,variance_bool=True,verbose=False)
		popt,pcov,chisq_red[i] = mt.gaussfit(x_meter,
				y,
				sigma_y=np.ones(len(y)),
				plot=False,
				variance_bool=True,
				verbose=False,
				background_bool=True)
		variance[i]         = popt[2]
		# print i
		varerr[i]           = pcov[2,2]
		stddev[i]           = np.sqrt(pcov[2,2])

	# ======================================
	# Set up basic beamline
	# ======================================
	emitx = 0.000100/gamma
	betax = .5
	alphax = -1 
	gammax = (1+np.power(alphax,2))/betax
	twiss = sltr.Twiss(beta=0.5,
		   alpha=0
		   )
	beamline=bt.beamlines.IP_to_lanex(twiss_x=twiss,twiss_y=twiss,gamma=gamma)
	beamline.elements[1].K1 = qs1_k_half
	beamline.elements[2].K1 = qs1_k_half
	beamline.elements[4].K1 = qs2_k_half
	beamline.elements[5].K1 = qs2_k_half
	
	# ======================================
	# Create beamline array??
	# ======================================
	gamma          = (1+davg)*39824
	beamline_array = np.array([])
	for i,gval in enumerate(gamma):
		beamline.gamma = gval
		beamline_array = np.append(beamline_array,copy.deepcopy(beamline))

	# ======================================
	# Fudge error
	# ======================================
	chisq_factor = 1e-28
	used_error   = chisq_factor*np.ones(len(stddev))

	# ======================================
	# Fit beamline
	# ======================================
	out = bt.fitBeamlineScan(beamline_array,
			variance,
			emitx,
			error=used_error,
			verbose=True)
	
	# ======================================
	# Plot results
	# ======================================
	bt.plotfit(davg,
			variance,
			out.beta,
			out.X_unweighted,
			top='Data is real!',
			figlabel='Comparison',
			error=used_error)


	# figchisquare = plt.figure()
	# plt.plot(davg,chisq_red)
	# mt.plot_featured(davg,chisq_red,'.-',
	#                 toplabel='Chi-Squared for Each Gaussian Fit',
	#                 xlabel='$E/E_0$',
	#                 ylabel='$\chi^2$')
	# print davg
	# print chisq_red

	_pdb.set_trace()

if __name__ == '__main__':
        parser=argparse.ArgumentParser(description=
                        'Wrap python analysis to be called at the command line.')
        parser.add_argument('-V',action='version',version='%(prog)s v0.2')
        parser.add_argument('-v','--verbose',action='store_true',
                        help='Verbose mode.')
        parser.add_argument('-o','--output',action='store',
                        help='Output filename. (Default: no file output.)')
        parser.add_argument('-i','--inputfile',
                        help='Input Matlab v7 file.',
			default='tempfiles/forpython.mat')
        parser.add_argument('-f','--fit', choices=['gauss', 'bigauss'], default='gauss', 
                        help='Type of fit to spot size profile. (Default: %(default)s)')
        arg=parser.parse_args()
        out=wrap_analyze(arg.inputfile)
        
        if arg.verbose:
                plt.show()
