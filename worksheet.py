#!/usr/bin/env python

from laser_on_off import *
import E200
import mytools as mt
import matplotlib.pyplot as plt
import numpy as np
import ipdb
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import re

import logging
loggerlevel = logging.DEBUG
logger=logging.getLogger(__name__)

fontsize=7
layout_rect = [0,0,1,0.95]

def worksheet(data,pdf,main_title):
    gs = gridspec.GridSpec(3,2)
    fig = plt.figure(figsize=(8.5,11))
    fig.suptitle(main_title.format(1))
    ax = fig.add_subplot(gs[0,0])

    #  data=E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537',local=True,readonly=True)
    
    dats      = E200.E200_api_getdat(data.wdrill.data.processed.scalars.ss_ELANEX_valid._hdf5)
    uids      = dats.UID[dats.dat==True]
    emit_dats = E200.E200_api_getdat(data.wdrill.data.processed.scalars.ss_ELANEX_emit_n._hdf5,UID=uids)
    
    imgstr = data.rdrill.data.raw.images.E224_Probe._hdf5
    
    laseron = laser_on_off(imgstr,uids)
    if not np.any(laseron==True):
        laser_on_exist = False
        logger.log(level=loggerlevel,msg='No laser on shots')
    else:
        laser_on_exist = True

    if not np.any(laseron==False):
        laser_off_exist = False
        logger.log(level=loggerlevel,msg='No laser off shots')
    else:
        laser_off_exist = True

    
    # =====================================
    # Create figure if no axes specified
    # =====================================
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

    # =====================================
    # Get Numbers
    # =====================================
    norm_emit_on     = emit_dats.dat[laseron==1]*1e6
    if len(norm_emit_on) > 0:
        avg_norm_emit_on = '{:0.3f}'.format(np.mean(norm_emit_on))
        std_norm_emit_on = '{:0.3f}'.format(np.std(norm_emit_on))
    else:
        avg_norm_emit_on = 'N/A'
        std_norm_emit_on = 'N/A'

    norm_emit_off     = emit_dats.dat[laseron==0]*1e6
    #  ipdb.set_trace()
    if len(norm_emit_off) > 0:
        avg_norm_emit_off = '{:0.3f}'.format(np.mean(norm_emit_off))
        std_norm_emit_off = '{:0.3f}'.format(np.std(norm_emit_off))
    else:
        avg_norm_emit_off = '(N/A)'
        std_norm_emit_off = '(N/A)'
    
    # =====================================
    # Plot logic
    # =====================================
    if laser_on_exist and laser_off_exist:
        out_plot = ax.plot(norm_emit_on,'.-',norm_emit_off,'.-')
        ax.legend(['Laser On','Laser Off'],fontsize=fontsize)
        mt.addlabel(toplabel = 'Effect of Laser on Emittance',axes=ax)

    elif laser_on_exist and laser_off_exist==False:
        out_plot = ax.plot(norm_emit_on,'.-')
        ax.legend(['Laser On'],fontsize=fontsize)
        toplabel = 'Effect of Laser on Emittance\nNO LASER OFF DATA'
        ax.set_title(toplabel,color='red')
    elif laser_on_exist==False and laser_off_exist:
        out_plot = ax.plot(norm_emit_off,'.-')
        ax.legend(['Laser On'],fontsize=fontsize)
        toplabel = 'Effect of Laser on Emittance\nNO LASER ON DATA'
        ax.set_title(toplabel,color='red')
    else:
        raise NotImplementedError('Check laser on/off arrays')

    
    mt.addlabel(
            axes     = ax,
            xlabel   = 'Unsorted Shots',
            ylabel   = 'Norm. Emittance [mm-mrad]')
    
    #  fig.tight_layout()
    #  
    #  plt.show()
    #  
    #  fig.savefig('NormEmit_Laser_On_Off_13537.jpg')
    mt.graphics.axesfontsize(ax,fontsize=7)

    ax = fig.add_subplot(gs[0,1])

    table_begin = r'''
        \begin{{tabular}}{{ll}}
        \toprule
        \multicolumn{{2}}{{c}}{{Laser On}} \\
        \midrule
        Average [mm-mrad] & {} \\
        Std. Dev. [mm-mrad] & {} \\
        \toprule
        \multicolumn{{2}}{{c}}{{Laser Off}} \\
        \midrule
        Average [mm-mrad] & {} \\
        Std. Dev. [mm-mrad] & {} \\
        \bottomrule
        \end{{tabular}}'''
    table_begin = table_begin.format(
            avg_norm_emit_on,
            std_norm_emit_on,
            avg_norm_emit_off,
            std_norm_emit_off
            )
    table_begin = re.sub('\\n',' ',table_begin)
    
    ax.text(0.5,1,table_begin,fontsize=fontsize,ha='center',va='top')
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.get_figure().tight_layout()

    gs.tight_layout(fig,rect=layout_rect)
    pdf.savefig(fig)
    return pdf
