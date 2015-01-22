#!/usr/bin/env python

from laser_on_off import *
import E200
import mytools as mt
import matplotlib.pyplot as plt

data=E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537',local=True,readonly=True)

dats      = E200.E200_api_getdat(data.wdrill.data.processed.scalars.ss_ELANEX_valid._hdf5)
uids      = dats.UID[dats.dat==True]
emit_dats = E200.E200_api_getdat(data.wdrill.data.processed.scalars.ss_ELANEX_emit_n._hdf5,UID=uids)

imgstr = data.rdrill.data.raw.images.E224_Probe._hdf5

laseron = laser_on_off(imgstr,uids)

# =====================================
# Laser on shots
# =====================================

norm_emit_on = emit_dats.dat[laseron==1]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(norm_emit_on*1e6,'.-')

# =====================================
# Laser off shots
# =====================================

norm_emit_off = emit_dats.dat[laseron==0]

ax.plot(norm_emit_off*1e6,'.-')
ax.legend(['Laser On','Laser Off'])

mt.addlabel(
        axes     = ax,
        toplabel = 'Dataset 13537, 06/29/2014',
        xlabel   = 'Unsorted Shots',
        ylabel   = 'Norm. Emittance [mm-mrad]')

fig.tight_layout()

plt.show()

fig.savefig('NormEmit_Laser_On_Off_13537.jpg')
