from laser_on_off import *
import E200
import mytools as mt
import matplotlib.pyplot as plt

data=E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537',local=True,readonly=True)

dats = E200.E200_api_getdat(data.wdrill.data.processed.scalars.ss_ELANEX_emit_n._hdf5)

imgstr = data.rdrill.data.raw.images.E224_Probe._hdf5

laseron = laser_on_off(imgstr,dats.UID)

# =====================================
# Laser on shots
# =====================================

norm_emit = dats.dat[laseron==1]

mt.plot_featured(norm_emit,'.-',legend=['Laser On'])

# =====================================
# Laser off shots
# =====================================

norm_emit = dats.dat[laseron==0]

mt.plot_featured(norm_emit,'.-',legend=['Laser On','Laser Off'])

plt.show()

