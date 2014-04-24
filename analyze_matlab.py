#!/usr/bin/env python

import argparse
import numpy as np
import scipy.io as sio
import ButterflyEmittancePython as bt
import mytools.slactrac as sltr
import matplotlib.pyplot as plt
import mytools as mt
import copy
import h5py as h5

plt.close()

# ======================================
# Load and transfer matlab variables
# ======================================
infile     = 'forpython.mat'
f          = h5.File(infile);
data       = f['data']
imgstr       = data['raw']['images']['CMOS_FAR']
res = imgstr['RESOLUTION'][0,0]

# ======================================
# Bend magnet strength
# ======================================
B5D36 = data['raw']['scalars']['LI20_LGPS_3330_BDES']['dat']
B5D36 = mt.derefdataset(B5D36,f)
B5D36_en  = B5D36[0]
new_en    = (B5D36_en-4.3)
gamma     = (B5D36_en/0.5109989)*1e3
new_gamma = (new_en/0.5109989)*1e3

# ======================================
# Translate into script params
# ======================================
# xstart = 350
# xstop  = 550
# ystart = 225
# ystop  = 280
n_rows    = 3
xstart = 275
xstop  = 325
ystart = 660
ystop  = 690
y_int = np.round((ystop-ystart)/n_rows)
y_vec = mt.linspacestep(ystart,ystop,y_int)
x_int = np.round((xstop-xstart)/n_rows)
x_vec = mt.linspacestep(xstart,xstop,x_int)
x_mean = np.mean(x_vec)
x_axis = (x_vec-x_mean)*res*10**(-3)

# ======================================
# Get image
# ======================================
# imgdat=mt.E200.E200_api_getdat(imgstr,f)
img=mt.E200.E200_load_images(imgstr,f)
img=img[8,xstart:xstop,ystart:ystop]
# plt.imshow(np.rot90(img,k=-1))
# plt.show()

# ======================================
# Create a histogram of std dev
# ======================================
hist_vec  = mt.linspacestep(ystart,ystop,n_rows)
n_groups  = np.size(hist_vec)
# hist_data = np.zeros([n_groups,2])
x_pix     = np.round(mt.linspacestep(xstart,xstop-1,1))
x_meter   = (x_pix-np.mean(x_pix)) * res * 10**-6
x_sq      = x_meter**2

num_pts = 11
variance  = np.zeros(num_pts)
stddev    = np.zeros(num_pts)
varerr    = np.zeros(num_pts)
chisq_red = np.zeros(num_pts)
for i in mt.linspacestep(1,n_groups-1):
	print i
	sum_x = np.sum(img[:,(i-1)*n_rows:i*n_rows],1)
	# plt.plot(x_meter,sum_x)
	# plt.show()
	popt,pcov,chisq_red[i] = mt.gaussfit(x_meter,sum_x,sigma_y=np.sqrt(sum_x),plot=False,variance_bool=True,verbose=True,background_bool=True)
	variance[i]         = popt[2]
	varerr[i]           = pcov[2,2]
	stddev[i]           = np.sqrt(pcov[2,2])


# davg         = (hist_data[:,0]-1)
# variance_old = hist_data[:,1]
# filt         = np.logical_not( (davg>(0.9971-1)) & (davg < (1.003-1)))
# filt         = np.logical_or(filt, np.logical_not(filt))

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
betax = 1
alphax = 0
gammax = (1+np.power(alphax,2))/betax
twiss    = sltr.Twiss(
		beta  = 0.5,
		alpha = 0
		)

# Create beamlines
beamline=bt.beamlines.IP_to_lanex(twiss_x=twiss,twiss_y=twiss,gamma=gamma)

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
