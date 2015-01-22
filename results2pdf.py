#!/usr/bin/env python
import pdb
import re
import E200
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import mytools as mt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
import matplotlib.pyplot as plt
from laser_on_off import *
import datetime as dt

import ButterflyEmittancePython as bt

from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')
rc('font', serif='cm')

# =====================================
# Load data
# =====================================
data=E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537',local=True,readonly=True)

processed_drill = data.wdrill.data.processed
scalars_drill   = processed_drill.scalars
vectors_drill   = processed_drill.vectors
arrays_drill    = processed_drill.arrays

scalars_rdrill = data.rdrill.data.raw.scalars

# =====================================
# Helper function
# =====================================
def get_str(drill):
    out_str = drill._hdf5
    return drill,out_str

# =====================================
# Get UIDs, energy axes, images, etc
# =====================================
valid = scalars_drill.ss_ELANEX_valid
uids = valid.UID[valid.dat==True]
#  uids = scalars_drill.ss_ELANEX_valid.UID
#  uids = uids[0:8]

valid_drill,valid_str               = get_str(scalars_drill.ss_ELANEX_valid)
valid                               = E200.E200_api_getdat(valid_str,uids)

quadval_drill,quadval_str           = get_str(scalars_rdrill.step_value)
quadval                             = E200.E200_api_getdat(quadval_str,uids)

emit_n_drill,emit_n_str             = get_str(scalars_drill.ss_ELANEX_emit_n)
emit_n                              = E200.E200_api_getdat(emit_n_str,uids)

betastar_drill,betastar_str         = get_str(scalars_drill.ss_ELANEX_betastar)
betastar                            = E200.E200_api_getdat(betastar_str,uids)

sstar_drill,sstar_str               = get_str(scalars_drill.ss_ELANEX_sstar)
sstar                               = E200.E200_api_getdat(sstar_str,uids)

rect_drill,rect_str                 = get_str(vectors_drill.ss_ELANEX_rect)
rects                               = E200.E200_api_getdat(rect_str,uids)

eaxis_drill,eaxis_str               = get_str(vectors_drill.ss_ELANEX_energy_axis)
eaxis                               = E200.E200_api_getdat(eaxis_str,uids)

variance_drill,variance_str         = get_str(vectors_drill.ss_ELANEX_variance)
variance                            = E200.E200_api_getdat(variance_str,uids)

beta_drill,beta_str                 = get_str(vectors_drill.ss_ELANEX_LLS_beta)
beta                                = E200.E200_api_getdat(beta_str,uids)

y_error_drill,y_error_str           = get_str(vectors_drill.ss_ELANEX_LLS_y_error)
y_error                             = E200.E200_api_getdat(y_error_str,uids)

X_unweighted_drill,X_unweighted_str = get_str(arrays_drill.ss_ELANEX_LLS_X_unweighted)
X_unweighted                        = E200.E200_api_getdat(X_unweighted_str,uids)

selected_img_drill,selected_img_str = get_str(arrays_drill.ss_ELANEX_selected_img)
selected_img                        = E200.E200_api_getdat(selected_img_str,uids)

oimg_eaxis_drill,oimg_eaxis_str     = get_str(vectors_drill.ss_ELANEX_oimg_eaxis)
oimg_eaxis                          = E200.E200_api_getdat(oimg_eaxis_str,uids)

elanex_drill,elanex_str             = get_str(data.rdrill.data.raw.images.ELANEX)
images                              = E200.E200_load_images(elanex_str,uids)

E224_Probe_drill,E224_Probe_str     = get_str(data.rdrill.data.raw.images.E224_Probe)

laseron = laser_on_off(E224_Probe_str,uids)

num_shots      = len(valid)
slots_per_page = 5
pages          = np.int(np.ceil(num_shots/np.float(slots_per_page)))

now = dt.datetime.now()

pdf = PdfPages('13537_processed_{}-{}-{}_{}-{}.pdf'.format(now.month,now.day,now.year,now.hour,now.minute))

# =====================================
# Basic formatting options
# =====================================
linewidth = 1
fontsize=7

# =====================================
# Create pages with slots_per_page
# number of analysis/page
# =====================================
for i in range(pages):
    gs = gridspec.GridSpec(5,3)
    fig = plt.figure(figsize=(8.5,11))
    fig.suptitle('Single Shot Emittance Analysis, Dataset 13537, Page {}/{}'.format(i+1,pages))

    # =====================================
    # Add analysis to each slot
    # =====================================
    for j in range(slots_per_page):
        indx = i*slots_per_page+j
        print indx
        # =====================================
        # Only add if there are shots left
        # =====================================
        if indx < num_shots:
            # =====================================
            # Plot Energy
            # =====================================
            img_to_plot = np.fliplr(np.rot90(images.images[indx]))
            uid = images.UID[indx]

            ax     = fig.add_subplot(gs[j,0])
            e_axis = oimg_eaxis.dat[indx]
            e_axis = np.flipud(e_axis)

            # =====================================
            # Get energy, pixel ranges
            # =====================================
            x_min = 1
            x_max = img_to_plot.shape[0]
            x_range = x_max-x_min

            y_min = e_axis[-1]
            y_max = e_axis[0]
            y_max = img_to_plot.shape[1]
            y_range = y_max-y_min

            aspect = x_range/y_range * img_to_plot.shape[1]/img_to_plot.shape[0]
            #  aspect = np.power(np.float64(img_to_plot.shape[1])/np.float64(img_to_plot.shape[0]),2)
            
            extent = (x_min,x_max,y_min,y_max)

            # =====================================
            # Show image
            # =====================================
            #  ax.imshow(img_to_plot,extent=extent,aspect=aspect,origin='lower')
            #  ax.imshow(img_to_plot,aspect=aspect,origin='lower')
            #  img = mpl.image.NonUniformImage(ax)
            #  img.set_data(e_axis,mt.linspacestep(1,x_max),img_to_plot)
            pixels = selected_img.dat[indx].flatten()
            hist,edges = np.histogram(pixels,bins=50)
            new_edges = edges[1:]
            max_count = np.max(new_edges[hist>50])
            img       = mt.NonUniformImage(e_axis,mt.linspacestep(1,x_max),img_to_plot,ax=ax)
            img.set_clim([0,max_count])
            mt.addlabel(axes=ax,ylabel='Pixels',xlabel='Energy [GeV]')
            cb=fig.colorbar(img)
            ax.tick_params(labelsize=fontsize)
            cb.ax.tick_params(labelsize=fontsize)
            ax.get_figure().tight_layout()

            # =====================================
            # Get rectangle info
            # =====================================
            thisrect = rects.dat[indx]

            # =====================================
            # Retool y to energy scale
            # =====================================
            x = thisrect[0]
            y = thisrect[1]
            width = thisrect[2]
            height=thisrect[3]

            myrect = mt.qt.Rectangle(*thisrect)
            y0 = myrect.x0
            y1 = myrect.x1
            temp = np.flipud(e_axis)
            e_y0 = temp[np.int(np.round(y0))]
            e_y1 = temp[np.int(np.round(y1))]
            e_width = e_y1-e_y0
            
            #  rect = mt.qt.Rectangle(x,e_y0,e_width,height,axes=ax,alpha=1,fill=False)
            rect = mt.qt.Rectangle(e_y0,y,e_width,height,axes=ax,alpha=1,fill=False)
            ax.add_patch(rect.get_rect())

            mt.graphics.less_labels(ax,y_fraction=1)
            mt.graphics.axesfontsize(ax,fontsize)

            # =====================================
            # Plot Fit
            # =====================================
            figlabel='Butterfly Fit'
            ax = fig.add_subplot(gs[j,1])
            ax0 = bt.plotfit(
                    eaxis.dat[indx],
                    variance.dat[indx],
                    beta.dat[indx],
                    X_unweighted.dat[indx],
                    top        = 'Emittance and Beam Parameter Fit',
                    figlabel   = figlabel,
                    bottom     = 'Energy [GeV]',
                    axes       = ax,
                    error      = y_error.dat[indx],
                    linewidth  = linewidth,
                    fontsize   = fontsize,
                    markersize = 2
                    )
            
            mt.graphics.less_labels(ax0,y_fraction=1)
            mt.graphics.axesfontsize(ax0,fontsize)

            ax0.get_figure().tight_layout()

            # =====================================
            # Add numbers
            # =====================================
            ax  = fig.add_subplot(gs[j,2])

            # Calculate pinch energy
            size         = np.dot(X_unweighted.dat[indx],beta.dat[indx])
            argmin       = np.argmin(size)
            pinch_energy = eaxis.dat[indx][argmin]

            if laseron[indx]:
                laser_status = 'On'
            else:
                laser_status = 'Off'

            table_begin = r'''
\begin{{tabular}}{{ll}}
\toprule
Date & {} \\
UID & {:0.0f} \\
Quad Offset [GeV] & {:0.3f} \\
\midrule Pinch Energy [GeV] & {:0.3f} \\
Norm Emit [mm-mrad] &  {:0.3f} \\
Beta* [m] &  {:0.3f} \\
S* [m] & {:0.3f} \\
Laser & {} \\
\bottomrule
\end{{tabular}}'''
            setdate='06/09/2014'
            table_begin = table_begin.format(
                    setdate,
                    uid,
                    quadval.dat[indx],
                    pinch_energy,
                    emit_n.dat[indx]*1e6,
                    betastar.dat[indx],
                    sstar.dat[indx],
                    laser_status
                    )
            table_begin = re.sub('\\n',' ',table_begin)

            #  table_begin = r'''\begin{tabular}{ c | c | c | c } & col1 & col2 & col3 \\\hline row1 & 11 & 12 & 13 \\\hline row2 & 21 & 22 & 23 \\\hline  row3 & 31 & 32 & 33 \end{tabular}'''
            ax.text(-0.1,0.25,table_begin,fontsize=fontsize)
            ax.set_frame_on(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            ax.get_figure().tight_layout()
            
            
    gs.tight_layout(fig,rect=[0,0,1,0.95])
    pdf.savefig(fig)
    plt.close()

pdf.close()
