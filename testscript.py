#!/usr/bin/env python

import numpy as np
import mytools as mt
import matplotlib.pyplot as plt
import h5py as h5

plt.close('all')

f            = h5.File('tempfiles/forpython.mat')
data         = f['data']

step_value   = data['raw']['scalars']['step_value']
zero_uids    = mt.E200_api_getUID(step_value, 0, f)

cegain       = data['raw']['images']['CEGAIN']
img_uids     = cegain['UID'][:, 0]

# wantedUIDs = np.intersect1d(img_uids, zero_uids)
wantedUIDs   = np.in1d(img_uids, zero_uids[16])

imgs         = cegain['dat'][:, 0]
img          = imgs[wantedUIDs]

this         = mt.E200_load_images(img, f)

step_uids    = step_value['UID'][:, 0]
stepbool     = np.in1d(step_uids, wantedUIDs)

plt.show()
