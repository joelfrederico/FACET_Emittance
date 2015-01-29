#!/usr/bin/env python
import ButterflyEmittancePython as bt
import mytools as mt
import numpy as np
import os
import shlex
import slactrac as sltr
import subprocess
import sys

import jinja2 as jj
import ipdb

logger = mt.mylogger(filename='worksheet')
# Set up initial beam
emitx = np.float(100e-6)
emity = emitx

beam_x = sltr.BeamParams(
        beta  = 0.5,
        alpha = 0,
        emit = emitx
        )
beam_y = sltr.BeamParams(
        beta  = 5,
        alpha = 0,
        emit = emity
        )

# Set up spectrometer quadrupoles
setQS = mt.hardcode.setQS(energy_offset=0)
QS1_K1 = setQS.QS1.K1
QS2_K1 = setQS.QS2.K1

# Get beamline for initial beam,
# spectrometer config
beamline=bt.beamlines.IP_to_lanex(
        beam_x = beam_x,
        beam_y = beam_y,
        QS1_K1 = QS1_K1,
        QS2_K1 = QS2_K1
        )

# beamline.elegant_lte(filename='drift.lte')
# 
# loader = jj.FileSystemLoader('templates')
# env = jj.Environment(loader=loader)
# 
# template = env.get_template('drift.ele')
# 
# template.stream(matched=0).dump('output.ele')

#  sltr.elegant_sim(beamline)
path = sltr.elegant_sim(beamline,dir=os.getcwdu())

command = 'open {}'.format(path)

subprocess.call(shlex.split(command))


