#!/usr/bin/env python

# System imports
import argparse
import copy
import h5py as h5
import pdb

# Math/science imports
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gs
import matplotlib as mpl
# mpl.rcParams.update({'font.size':7})

# My module imports
import ButterflyEmittancePython as bt
import mytools.slactrac as sltr
import mytools as mt
import mytools.E200 as E200

# Allow for standalone iPython debugging.
# import sys
# from IPython.core import ultratb
# sys.excepthook = ultratb.FormattedTB(mode='Verbose',
# color_scheme='Linux', call_pdb=1)

plt.close('all')
def wrap_analyze(infile):
	# ======================================
	# Start PDF creation
	# ======================================
	# Create PDF
	pp = PdfPages('output.pdf')
	# Create figure
	fig=mt.figure('Page 1',figsize=(8.5,11))
	# Create larger gridspec
	outergs= gs.GridSpec(4,1)

	# ======================================
	# Load and transfer matlab variables
	# ======================================
	f=h5.File(infile)
	data=f['data']
	
	# ======================================
	# Get step info and setup
	# ======================================
	step_value=data['raw']['scalars']['step_value']
	step_vals=np.unique(E200.E200_api_getdat(step_value,f))
	# Artificially limit step_vals to =0GeV
	step_vals=np.array([0])
	numvals = step_vals.shape[0]
	emit_array=np.zeros((numvals,50))

	# for i,stepval in enumerate(step_vals[2:]):
	# ======================================
	# Run over steps
	# ======================================
	for i,stepval in enumerate(step_vals):
		print 'We\'re on step {} with value {}.'.format(i,stepval)

		zero_uids=mt.E200.E200_api_getUID(step_value,stepval,f)
		print zero_uids
		cegain = data['raw']['images']['CEGAIN']
		img_uids=cegain['UID'][:,0]
		# wantedUIDs=zero_uids[16]
		valid_img_uids=np.intersect1d(zero_uids,img_uids)
		for j,stepuid in enumerate(valid_img_uids[0:5]):
			try:
				# ======================================
				# Save all figs to one page
				# ======================================
				# Use correct line
				linnum=np.mod(j,4)
				if linnum == 0:
					if j>0:
						outergs.tight_layout(fig)
						pp.savefig(figure=fig)
					plt.close('all')
					fig=mt.figure('Steps {}-{}'.format(j+1,j+5),figsize=(8.5,11))
				innergs=gs.GridSpecFromSubplotSpec(1,2,subplot_spec=outergs[linnum])
				aximg=plt.Subplot(fig,innergs[0,0])
				axplotfit=plt.Subplot(fig,innergs[0,1])
				# pdb.set_trace()
				# pp.savefig()
				out = single_analysis(
						data,
						stepuid,
						f,
						aximg=aximg,
						axplotfit=axplotfit
						)
				fig.add_subplot(aximg)
				fig.add_subplot(axplotfit)
				# innergs.tight_layout(fig)
				# outergs.tight_layout(fig)
				emit_array[i,j]=out.emit
				# plt.show()
				# plt.clear('all')
				# pdb.set_trace()
				
			except KeyboardInterrupt:
				raise
			except:
				# raise
				pass


		if i > 0:
			pdb.set_trace()

	# pdb.set_trace()
	outergs.tight_layout(fig)
	pp.savefig(figure=fig)
	pp.close()
	return emit_array


def single_analysis(data,wantedUIDs,f,plot=False,aximg=None,axplotfit=None):
	# ======================================
	# Set up plots and PDF saving
	# ======================================
	if plot:
		plt.close('all')

	# ======================================
	# Load the right image
	# ======================================
	cegain = data['raw']['images']['CEGAIN']
	img_uids=cegain['UID'][:,0]
	wantedUIDs_bool=np.in1d(img_uids,wantedUIDs)
	imgs=cegain['dat'][:,0]
	img=imgs[wantedUIDs_bool]
	img=mt.E200.E200_load_images(img,f)
	img=img[0]
	# Show image loaded
	if plot:
		plt.imshow(img)
		if plot:
			plt.show()

	if aximg is not None:
		aximg.imshow(img)
		mt.figure('this')
		plt.imshow(img)
		# plt.show()

	# ======================================
	# Set up image slices
	# ======================================
	res_y    = 10.3934e-6
	res_x    = res_y / np.sqrt(2)

	# ======================================
	# Load quad values
	# ======================================
	step_value=data['raw']['scalars']['step_value']
	# step_uids=step_value['UID'][:,0]
	step_vals=E200.E200_api_getdat(step_value,f,wantedUIDs)
	E_offset=step_vals[0]

	# ======================================
	# Image slice setup
	#	-Use ~2% bandwidth
	# ======================================
	E0    = 20.35 + E_offset
	# bandE = 0.01*E0
	bandE = 0.008*E0
	Emin  = E0-bandE
	Emax  = E0+bandE
	# Corresponding y window
	y_min = bt.E_to_y(Emin,f,res_y)
	y_max = bt.E_to_y(Emax,f,res_y)

	# Get image size and corresponding
	# y-axis -> energy
	ysize,xsize=img.shape

	# x_min starts at 200 to avoid cam region
	# that has no counts, on the left.
	# Right side doesn't have this issue.
	x_min = 200
	x_max = xsize
	# More realistic bounds
	x_min = 500
	x_max = 750

	# ======================================
	# Plot image
	# ======================================
	if plot:
		fig=mt.figure('Roi\'d image')
		plt.imshow(img[y_min:y_max,x_min:x_max])
		pdb.set_trace()
		if plot:
			plt.show()
	
	# ======================================
	# Find the pinch
	# ======================================
	# mt.findpinch(
	#                 img,
	#                 xbounds=(x_min,x_max),
	#                 ybounds=(y_min,y_max),
	#                 step=2,
	#                 verbose=True)

	# ======================================
	# Define strip edges.
	# ======================================
	# Number of strips should be odd so the
	# center strip is at E0.
	num_strips = 11
	# There are +1 edges than strips in y.
	E_edges = np.linspace(Emin,Emax,num_strips+1)
	x_edges = mt.linspacestep(x_min,x_max)

	# ======================================
	# Get spot sizes for strips (new)
	# ======================================
	variance  = np.zeros(num_strips)
	stddev    = np.zeros(num_strips)
	varerr    = np.zeros(num_strips)
	chisq_red = np.zeros(num_strips)
	eavg      = np.zeros(num_strips)
	for i in mt.linspacestep(0,num_strips-1):
		# Get low/high energy edges
		Elow  = E_edges[i]
		Ehigh = E_edges[i+1]
		
		# Convert to y values
		ylow  = bt.E_to_y(Elow,f,res_y)
		yhigh = bt.E_to_y(Ehigh,f,res_y)
		eavg[i], gaussout = mt.fitimageslice(
				img,
				res_x,
				res_y,
				(x_min,x_max),
				(ylow,yhigh),
				avg_e_func=bt.avg_E,
				h5file=f,
				plot=False)

		chisq_red[i] = gaussout.chisq_red
		variance[i]         = gaussout.popt[2]
		try:
			varerr[i]           = gaussout.pcov[2,2]
			stddev[i]           = np.sqrt(gaussout.pcov[2,2])
		except:
			print 'Error with gaussout.pcovp[2,2].'
			print 'Value of gaussout is {}.'.format(gaussout)

	davg=eavg/20.35 - 1
	# pdb.set_trace()

	# ======================================
	# Set up basic beamline
	# ======================================
	# ----------------
	# Get energy
	# ----------------
	B_spect = f[f['data']['raw']['scalars']['LI20_LGPS_3330_BDES']['dat'][0,0]][0,0]
	gamma     = (20.35/0.5109989)*1e3

	emitx = 0.000100/gamma
	betax = 0.5
	alphax = -1 
	gammax = (1+np.power(alphax,2))/betax
	twiss = sltr.Twiss(beta=0.5,
		   alpha=0
		   )
	beamline=bt.beamlines.IP_to_lanex(twiss_x=twiss,twiss_y=twiss,gamma=gamma)


	print step_vals[0]

	bact = E200.setQS.set_QS_energy_ELANEX(step_vals[0])
	qs1_k_half = E200.setQS.bdes2K1(bact[0],20.35)
	qs2_k_half = E200.setQS.bdes2K1(bact[1],20.35)

	beamline.elements[1].K1 = qs1_k_half
	beamline.elements[2].K1 = qs1_k_half
	beamline.elements[4].K1 = qs2_k_half
	beamline.elements[5].K1 = qs2_k_half

	# pdb.set_trace()
	
	# ======================================
	# Create beamline array
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
			verbose=True,
			plot=False
			)
	
	# ======================================
	# Plot results
	# ======================================
	bt.plotfit(davg,
			variance,
			out.beta,
			out.X_unweighted,
			top='Shot',
			figlabel='Comparison',
			figpath='figs',
			error=used_error,
			axes=axplotfit
			)

	# pdb.set_trace()

	return out

	# figchisquare = plt.figure()
	# plt.plot(davg,chisq_red)
	# mt.plot_featured(davg,chisq_red,'.-',
	#                 toplabel='Chi-Squared for Each Gaussian Fit',
	#                 xlabel='$E/E_0$',
	#                 ylabel='$\chi^2$')
	# print davg
	# print chisq_red

	# pdb.set_trace()

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
