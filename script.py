#!/usr/bin/env python
import sdds
import scipy as sp
import scipy.optimize as spopt
import numpy as np
import sddsToolkit as st
import mytools as mt
import matplotlib.pyplot as plt
import mytools.slactrac as sltr

plt.close('all')

out = st.loadpage('drift.out')
# x = st.sdds2array(out,'x') * 1000
# y = st.sdds2array(out,'y') * 1000
x = st.sdds2array(out,'x')
y = st.sdds2array(out,'y')
d = st.sdds2array(out,'d')
res = 100

# # Dispersion
# fig = plt.figure()
# top='Dispersion at Measurement'
# mt.hist2d(y,d,labels=[top,'y [mm]','$\delta$'],bins=res,fig=fig)
# plt.savefig('{}.eps'.format(top).replace(" ",""))

# Simulated Measurement
fig2 = plt.figure()
top='Simulated Measurement'
mt.hist2d(x,y,labels=[top,'x [mm]','y [mm]'],bins=res,fig=fig2)
# mt.hist2d(x,d,labels=[top,'x [mm]','$\delta$'],bins=res,fig=fig2)
plt.savefig('{}.eps'.format(top).replace(" ",""))

# # Ideal Measurement
# fig3 = plt.figure()
# top = 'Simulated Ideal Measurement'
# mt.hist2d(x,d,labels=[top,'x [mm]','$\delta$'],bins=res,fig=fig3)
# plt.savefig('{}.eps'.format(top).replace(" ",""))

# # Twiss Parameters
# twiss=st.loadpage('drift.twi')
# s = st.sdds2array(twiss,'s')
# bx = st.sdds2array(twiss,'betax')
# nx = st.sdds2array(twiss,'etax')*np.power(10,3)
# ny = st.sdds2array(twiss,'etay')*np.power(10,3)

# # Dispersion Measurement
# fig4 = plt.figure()
# # plt.plot(s,bx)
# plt.plot(s,nx,s,ny)
# top = 'Dispersion from Plasma Exit to Measurement'
# mt.addlabel(top,'Distance [m]','Dispersion [mm]')
# plt.savefig('{}.eps'.format(top).replace(" ",""))

# Spot size strips
h,xe,ye=np.histogram2d(x,d,res)
xval = (xe[1]-xe[0])/2. + xe
xval = xval[0:-1]
davg=(ye[1]-ye[0])/2. + ye
davg=davg[0:-1]

stddevsq=np.zeros(res)
indivbool = False
if indivbool: figscan = plt.figure()

def gauss(x,A,mu,sig):
	return A*np.exp(-np.power(x-mu,2)/(2*np.power(sig,2)))


for i,row in enumerate(np.transpose(h)):
	A = max(row)
	mean = np.sum(xval*row)/row.sum()
	var = np.sum(np.power(xval-mean,2)*row)/row.sum()
	root = np.sqrt(var)
	pguess = [A,mean,root]
	popt = pguess
	popt, pcov = spopt.curve_fit(gauss,xval,row,pguess)
	# print "A: {}, mean: {}, sig: {}".format(popt[0],popt[1],popt[2])
	# print "Percent diff: {}%".format(100*(popt[2]-root)/root)
	fit = gauss(xval,popt[0],popt[1],popt[2])
	unchangedroot = gauss(xval,popt[0],popt[1],root)
	if indivbool: plt.plot(xval,row,xval,fit,xval,unchangedroot)

	# plt.plot(xval,row)
	if indivbool: raw_input("Any key.")
	if indivbool: figscan.clf()
	# stddevsq[i] = np.power(popt[2],2)
	stddevsq[i] = var

stddev=np.sqrt(stddevsq)

filt=(davg>-0.015) & (davg < 0.015)
# fig5=plt.figure()
# plt.plot(davg[filt],stddev[filt])
# top='Spot Size for Energy'
# mt.addlabel(top,'$\delta$','$\sigma$')
# plt.savefig('{}.eps'.format(top).replace(" ",""))

# Simulation/Measurement

DRIFT1 = sltr.Drift(length=5.8996)
DRIFT2 = sltr.Drift(length=4)
DRIFT3 = sltr.Drift(length=0.73182)
DRIFT4 = sltr.Drift(length=11.2901)

QS1 = sltr.Quad(
		length= 5.000000000E-01,
		K1= 2.959427141E-01 * 0.977
		)
QS2 = sltr.Quad(
		length= 5.000000000E-01,
		K1=-2.227412494E-01 * 0.977
		)

B5D36 = sltr.Bend(
		length=9.779000000E-01,
		angle=6.000000000E-03,
		order=1,
		rotate=0
		)

beamline = sltr.Beamline(
                element_list=[DRIFT1,QS1,QS1,DRIFT2,QS2,QS2,DRIFT3,B5D36,DRIFT4],
                gamma=45000
                )

beamline.calc_mat()

# print "Quad"
# print beamline.elements[1]._K1
# print beamline.elements[1]._R

# print "Bend"
# print beamline.elements[7]._angle
# print beamline.elements[7]._R

# print "Drift"
# print beamline.elements[8]._R

# print "Total"
# print beamline.R

# beamline.change_energy(40000)
# beamline.calc_mat()

# print "Quad"
# print beamline.elements[1]._K1
# print beamline.elements[1]._R

# print "Bend"
# print beamline.elements[7]._angle
# print beamline.elements[7]._R

# print "Drift"
# print beamline.elements[8]._R

# print "Total"
# print beamline.R

# Calculate Matrices
# beta = (X^T X)^-1 X^T y

gamma = (1+davg[filt])*45000

y=stddevsq[filt]
y=y[np.newaxis]

X            = np.zeros([len(gamma),3])
# spot         = np.zeros(len(gamma))
spotexpected = np.zeros(len(gamma))

# # From algorithm results
# betax  = 0.0906270509998
# alphax = -0.433767228357
# gammax = (1+np.power(alphax,2))/betax
# emitx  = 8.70879128233e-10

# From sddsprocess results
emitx = 1.326446e-9
betax = 59.69009e-3
alphax = -0.7705554
gammax = (1+np.power(alphax,2))/betax
T = np.array([[betax,-alphax],[-alphax,gammax]])

print 'Emittance is {}.'.format(emitx)
print 'Normalized emittance is {}.'.format(emitx*45000)
print 'Initial beta should be {}.'.format(betax)
print 'Initial alpha should be {}.'.format(alphax)
print 'Initial gamma should be {}.'.format(gammax)
print '------------------------------'

R = np.zeros([6,6,len(gamma)])
betaf = np.zeros(len(gamma))
for i,g in enumerate(gamma):
	beamline.change_energy(g)
	beamline.calc_mat()
	R11 = beamline.R[0,0]
	R12 = beamline.R[0,1]
	R[:,:,i] = beamline.R
	X[i,0] = R11*R11
	X[i,1] = 2*R11*R12
	X[i,2] = R12*R12
	T2 = np.dot(np.dot(R[0:2,0:2,i],T),np.transpose(R[0:2,0:2,i]))
	betaf[i] = T2[0,0]
	spotexpected[i] = np.sqrt((R11*R11*betax - 2*R11*R12*alphax + R12*R12*gammax)*emitx)

beta = np.dot(np.linalg.pinv(X) , y.transpose())
print beta

emit = np.sqrt( beta[0,0] * beta[2,0] - np.square(beta[1,0]) )
beta0 = beta[0,0]/emit
gamma0 = beta[2,0]/emit
alpha0 = -np.sign(beta[1,0])*np.sqrt(beta0*gamma0-1)
print 'Emittance is {}.'.format(emit)
print 'Normalized emittance is {}.'.format(emit*45000)
print 'Initial beta should be {}.'.format(beta0)
print 'Initial alpha should be {}.'.format(alpha0)
print 'Initial gamma should be {}.'.format(gamma0)
print 'Initial spot should be {}.'.format(np.sqrt(beta[0,0]))

figres=plt.figure()
# plt.plot(davg[filt],stddev[filt],davg[filt],np.sqrt(np.dot(X,beta)))
plt.plot(davg[filt],stddev[filt],davg[filt],np.sqrt(np.dot(X,beta)),davg[filt],spotexpected)
# plt.plot(davg[filt],stddev[filt],davg[filt],spotexpected)
# plt.plot(davg[filt],spotexpected)
top='Spot Size for Energy'
mt.addlabel(top,'$\delta$','$\sigma$')

# figbeta=plt.figure()
# plt.plot(davg[filt],np.sqrt(betaf*emitx)*1e6,'.')

mt.graphics.tile()
