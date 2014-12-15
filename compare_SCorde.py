#!/usr/bin/env python
#!/usr/bin/env python #-m pdb

# import sys
# from IPython.core import ultratb
# sys.excepthook = ultratb.FormattedTB(mode='Verbose',
# color_scheme='Linux', call_pdb=1)

import E200
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import mytools as mt
import numpy as np
import scipy.io

import logging
logger = mt.mylogger(filename='compare_SCorde')

filebase = 'E200_13450'
dataset = '13438'
filebase = 'E200_{}'.format(dataset)
filename = '{}.mat'.format(filebase)

f = scipy.io.loadmat(filename)

# g = h5.File(filename,'r',driver='core',backing_store=False)

camname = f[filebase].dtype.names[0]
cam     = f[filebase][camname][0,0]

# ======================================
# Get Sebastien's emittance, UID
# ======================================
uid_scorde      = np.uint64(cam['UID'][0,0].flatten())
emit_n_scorde   = cam['norm_emittance'][0,0].flatten() * 1e-6
betastar_scorde = cam['beta_star'][0,0].flatten()
sstar_scorde    = cam['s_star'][0,0].flatten()
pinch_E_scorde  = cam['pinch_energy'][0,0].flatten()

# ======================================
# Sort by UID
# ======================================
ind_sort        = np.argsort(uid_scorde)

uid_scorde      = uid_scorde[ind_sort]
emit_n_scorde   = emit_n_scorde[ind_sort]
betastar_scorde = betastar_scorde[ind_sort]
sstar_scorde    = sstar_scorde[ind_sort]

# ======================================
# Set up and get my emittance, UID
# ======================================
sets = [['20140625',filebase]]
pair = sets[0]

setdate   = pair[0]
setnumber = pair[1]
loadfile  = 'nas/nas-li20-pm00/E200/2014/{}/{}'.format(setdate,setnumber)

data      = E200.E200_load_data(loadfile,readonly=True)
wf        = data.write_file
processed = wf['data']['processed']
vectors   = processed['vectors']
arrays    = processed['arrays']
scalars   = processed['scalars']

emit_n_str   = scalars['ss_{}_emit_n'.format(camname)]
emit_n       = E200.E200_api_getdat(emit_n_str,uid_scorde)

betastar_str = scalars['ss_{}_betastar'.format(camname)]
betastar     = E200.E200_api_getdat(betastar_str,uid_scorde)

sstar_str    = scalars['ss_{}_sstar'.format(camname)]
sstar        = E200.E200_api_getdat(sstar_str,uid_scorde)

# ======================================
# Get only overlapping data from SCorde
# ======================================
ind             = np.in1d(uid_scorde,emit_n.UID)

uid_scorde      = uid_scorde[ind]
emit_n_scorde   = emit_n_scorde[ind]
betastar_scorde = betastar_scorde[ind]
sstar_scorde    = sstar_scorde[ind]

# ======================================
# Get delta and plot histogram
# ======================================
# del_emit_n   = (emit_n_scorde-emit_n.dat)/emit_n.dat
# del_betastar = (betastar_scorde-betastar.dat)/betastar.dat
# del_sstar    = (sstar_scorde-sstar.dat)/sstar.dat

def plotfuncs(mydata,corde_data,toplabel):
    x        = np.float64(mydata)
    y        = corde_data
    del_data = x-y

    fig = plt.figure()
    ax  = fig.add_subplot(1,2,1)
    #  mt.hist(del_data,bins=20,range=(-1,1),ax=ax)
    mt.hist(del_data,bins=20,ax=ax)
    mt.addlabel(toplabel=toplabel)
    
    z  = np.polyfit(x,y,1)
    p2 = np.poly1d([1,0])
    
    #  fig = plt.figure()
    ax  = fig.add_subplot(1,2,2)
    ax.plot(x,y,'.',x,p2(x),'r')
    mt.addlabel(toplabel=toplabel)

plotfuncs(emit_n.dat,emit_n_scorde,toplabel='Normalized Emittance')
plotfuncs(betastar.dat,betastar_scorde,toplabel='Beta*')
plotfuncs(sstar.dat,sstar_scorde,toplabel='s*')

#  plt.show()
plt.close('all')

# ======================================
# Get Corde's energy
# ======================================

import corde_energy as ce

if camname == 'ELANEX':
    setQS=1.5
    y_scorde,energy_scorde = ce.Energy_Axis_ELANEX(13438,setQS)
elif camname == 'CMOS_FAR':
    pass
    # y_scorde,energy_scorde = ce.Energy_Axis_CMOS_FAR(13438,1.5)
else:
    raise NotImplementedError('Camera name is not available: {}'.format(camname))
energy_scorde = np.flipud(energy_scorde)

# ======================================
# Get my energy
# ======================================

rf = data.read_file
data_rf = rf['data']

# myenergy,myenergy_approx = E200.eaxis(y=y_scorde, uid=uid_scorde[0], camname=camname, hdf5_data=data_rf, E0=20.35, etay=0, etapy=0)
myenergy_approx = E200.Energy_Axis(camname=camname,hdf5_data=data_rf,uid=uid_scorde[0]).energy(ypx=y_scorde)

fig_en = plt.figure()
mygs = gs.GridSpec(1,1)
ax1 = fig_en.add_subplot(mygs[0])
plots=ax1.plot(y_scorde,energy_scorde,'b',y_scorde,myenergy_approx,'r')
# plots=ax1.plot(y_scorde,myenergy_approx,'g')
# plots=ax1.plot(y_scorde,energy_scorde,'b')

# plots[0].set_label('Sebastien')
# plots[1].set_label('Joel')
# ax1.legend()
# ax1.set_yscale('log')

mt.addlabel(toplabel=camname,xlabel='Pixels',ylabel='Energy [GeV]',axes=ax1)

plt.show()
