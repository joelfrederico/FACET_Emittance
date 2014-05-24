import scipy as sp
import numpy as np

def derivative(func, x0, tol=1e-3, verbose=False, *args, **kwargs):

	dx=x0/100.

	delta = tol*2
	
	while np.abs(delta) > tol:
		dx=dx/2
		deriv=sp.misc.derivative(func,x0,dx=dx)
		deriv2=sp.misc.derivative(func,x0,dx=dx/2)
		delta = deriv2-deriv

	if verbose:
		print 'Tol is {}, delta is {}, dx is {}'.format(tol, delta, dx)
	return deriv2

def testfunc(x):
	return np.sin(x)

# print derivative(testfunc,np.pi)
