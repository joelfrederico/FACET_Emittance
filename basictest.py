#!/usr/bin/env python -m pdb

from PyQt4 import QtGui,QtCore
import ButterflyEmittancePython as bt
import E200 as E200
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np

mt.mylogger('basictest')

try:
	data_a.close()
	data_b.close()
except:
	pass

# ======================================
# Diagnose set A
# ======================================
set_a        = ['20140625','13438']
emit_n_str_a = 'ss_ELANEX_emit_n'

setdate     = set_a[0]
setnumber   = set_a[1]
loadfile    = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
data_a      = E200.E200_load_data(loadfile)
wf_a        = data_a.write_file
processed_a = wf_a['data']['processed']
vectors_a   = processed_a['vectors']
arrays_a    = processed_a['arrays']
scalars_a   = processed_a['scalars']

emit_n_a_str = scalars_a[emit_n_str_a]
emit_n_a     = E200.E200_api_getdat(emit_n_a_str)
print emit_n_a.UID
emit_n_a     = E200.E200_api_getdat(emit_n_a_str,emit_n_a.UID[0])

# ======================================
# Diagnose set B
# ======================================
set_b        = ['20140629','13537']
emit_n_str_b = 'ss_ELANEX_emit_n'

setdate     = set_b[0]
setnumber   = set_b[1]
loadfile    = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate,setnumber)
data_b      = E200.E200_load_data(loadfile)
wf_b        = data_b.write_file
processed_b = wf_b['data']['processed']
vectors_b   = processed_b['vectors']
arrays_b    = processed_b['arrays']
scalars_b   = processed_b['scalars']

emit_n_b_str = scalars_b[emit_n_str_b]
emit_n_b     = E200.E200_api_getdat(emit_n_b_str)
emit_n_b     = E200.E200_api_getdat(emit_n_b_str,emit_n_b.UID[0])
