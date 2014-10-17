#!/usr/bin/env python

import mytools as mt
import mytools.qt as myqt
from PyQt4 import QtGui,QtCore
import h5py as h5
import numpy as np
import ButterflyEmittancePython as bt
import matplotlib.pyplot as plt
import matplotlib as mpl

wf                  = h5.File('data.hdf5','w')
wf.attrs['origin']  = 'python-h5py'
wf.attrs['version'] = h5.version.version
data                = wf.create_group('data')
processed           = data.create_group('processed')
scalars             = processed.create_group('scalars')
vectors             = processed.create_group('vectors')
arrays              = processed.create_group('arrays')

# ======================================
# Scalar test
# ======================================
# Set up new things for scalar
# verbose = True
verbose = False
if verbose:
	print r'''
=================================
Scalar test
================================='''
test_scalar = mt.E200.E200_create_data(scalars,'test_scalar',datatype='array')
test_uids   = np.array([6,7,8,1,4,5])
test_values = np.array(test_uids*1.1,dtype=np.float64)

# Add scalars
mt.E200.E200_api_updateUID(test_scalar,test_uids,test_values,verbose=verbose)

# Show scalars
if verbose:
	print test_scalar['UID'].value
	for val in test_scalar['dat'].value:
		print test_scalar.file[val].value

# Change scalars
test_uids   = np.array([9,6])
test_values = np.array(test_uids*-1.1,dtype=np.float64)

# Update scalars
mt.E200.E200_api_updateUID(test_scalar,test_uids,test_values,verbose=verbose)

# Show scalars
if verbose:
	print test_scalar['UID'].value
	for val in test_scalar['dat'].value:
		print test_scalar.file[val].value

# ======================================
# Vector test
# ======================================
# Set up new things for vector
verbose = True
# verbose = False
if verbose:
	print r'''
=================================
Vector test
================================='''
test_vector = mt.E200.E200_create_data(vectors,'test_vector',datatype='array')
test_uids   = np.array([6,7,8,1,4,5])
base = np.array([1,10,100],dtype=np.float64)
test_values = np.array(np.outer(test_uids,base),dtype=np.float64)

# Add vectors
mt.E200.E200_api_updateUID(test_vector,test_uids,test_values,verbose=verbose)

# Show vectors
if verbose:
	print test_vector['UID'].value
	for val in test_vector['dat'].value:
		print test_vector.file[val].value

# Change vectors
test_uids   = np.array([9,6])
base = np.array([1,10],dtype=np.float64)*-1
test_values = np.array(np.outer(test_uids,base),dtype=np.float64)

# Update vectors
mt.E200.E200_api_updateUID(test_vector,test_uids,test_values,verbose=verbose)

# Show vectors
if verbose:
	print test_vector['UID'].value
	for val in test_vector['dat'].value:
		print test_vector.file[val].value

# Show
wanted_uids = np.array([9,7,4])
returned_dat = mt.E200.E200_api_getdat(test_vector,uids=wanted_uids,verbose=True)
if verbose:
	print '\tReturned info:'
	print returned_dat.UID
	print returned_dat.dat


# ======================================
# Array test
# ======================================
# Set up new things for array
# verbose = True
verbose = False
if verbose:
	print r'''
=================================
Array test
================================='''
test_array = mt.E200.E200_create_data(arrays,'test_array',datatype='array')
test_uids   = np.array([6,7,8,1,4,5])
base_array = np.array([[1,10],[100,1000]])
test_values = np.empty(test_uids.shape,dtype=np.object)
for i,val in enumerate(test_uids):
	test_values[i] = base_array*val

# Add arrays
mt.E200.E200_api_updateUID(test_array,test_uids,test_values,verbose=verbose)

# Show arrays
if verbose:
	print test_array['UID'].value
	for val in test_array['dat'].value:
		print test_array.file[val].value

# Change arrays
test_uids   = np.array([9,6])
base_array = np.array([[1,10,100],[-100,-10,-1]])
test_values = np.empty(test_uids.shape,dtype=np.object)
for i,val in enumerate(test_uids):
	test_values[i] = base_array*val

# Update arrays
mt.E200.E200_api_updateUID(test_array,test_uids,test_values,verbose=verbose)

# Show arrays
if verbose:
	print test_array['UID'].value
	for val in test_array['dat'].value:
		print test_array.file[val].value
