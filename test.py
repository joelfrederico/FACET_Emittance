#!/bin/env python
import mytools as mt
import numpy as np

y=np.linspace(1,600,600)
out=mt.E200.eaxis(y=y,res=60e-6,E0=20.35,etay=0,etapy=0,ypinch=260)

Lmag = 2*4.889500000E-01
Ldrift=8.792573 + 0.8198
# E=20.35
E0=20.35
theta=6e-3
ypinch=260
res=60e-6
eta0=0
etap0=0

# y=
