import mytools as mt
import numpy as np
import pdb

#  logger = mt.mylogger(filename='reprocess')
import logging
loggerlevel = logging.DEBUG
logger=logging.getLogger(__name__)

# Energy axis for the data of the high-gradient positron acceleration letter.
# Only for ELANEX camera.

# Sebastien Corde
# Create: October 28, 2014
# Last edit: October 29, 2014

# Example of usage:
# E = Energy_Axis_ELANEX('13450', 4.5)
# returns the energy axis E (for all ELANEX camera pixels, 1:734) for
# dataset E200_13450 and for QS = 4.5 GeV.

def Energy_Axis_ELANEX(dataset, QS):

    # Values below are for CMOS FAR
    if dataset == 13437 or dataset == 13438:
        y0    = np.float128(1589.0) # pixel position of E0 (20.35 GeV).
        eta_0 = np.float128(949.72) # nominal dipole dispersion in pixel, corresponding to 59.5 mm.
        
    elif dataset == 13448 or dataset == 13449:
        y0    = np.float128(1605.5 - 0.7923*(20.35+QS)   ) # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(949.72 + (20.35+QS) * 0.7923 ) # added QS dispersion of 0.7923 pix per QS GeV.
            
    elif dataset == 13450:
        y0    = np.float128(1655 - 3.321*(20.35+QS)     ) # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(949.72 + (20.35+QS) * 3.321 ) # added QS dispersion of 3.321 pix per QS GeV.
        
    elif dataset == 13537:
        y0    = np.float128(576 + 0.5193*(20.35+QS)     ) # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(49.72 - (20.35+QS) * 0.5193 ) # added QS dispersion of -0.5193 pix per QS GeV.
    else:
        logger.error('This dataset does not have a calibrated energy axis. Returning the nominal energy axis.')
        y0    = np.float128(1590   ) # pixel position of E0 (20.35 GeV).
        eta_0 = np.float128(949.72 ) # nominal dipole dispersion in pixel, corresponding to 59.5 mm.
    
    # Converting these values to ELANEX (different z location and different calibration)
    
    z_B5D36    = np.float128(2005.65085 ) # middle of dipole magnet
    z_ELANEX   = np.float128(2015.22    ) # linac z location of ELANEX phosphor screen in meter
    z_CFAR     = np.float128(2016.04    ) # linac z location of Cherenkov Far gap in meter
    cal_ELANEX = np.float128(8.9185     ) # ELANEX camera calibration in um/pixel
    cal_CFAR   = np.float128(62.65      ) # CMOS FAR camera calibration in um/pixel

    # y0 = 259 (when QS=0) at ELANEX corresponds to y0 = 1589 on CMOS FAR.
    y0    = np.float128(259) + (cal_CFAR/cal_ELANEX) * (y0-np.float128(1589))
    eta_0 = (cal_CFAR/cal_ELANEX) * (z_ELANEX-z_B5D36) / (z_CFAR-z_B5D36) * eta_0
    
    y      = np.linspace(-6000,6000,num=12001,dtype=np.float128)
    E0     = np.float128(20.35)
    E_FULL = E0 / ( np.float128(1) - y/eta_0 )
    
    delta_y = np.floor(np.float128(55)*QS/(QS+E0) / (np.float128(1e-3) * cal_ELANEX))
    
    i1_compare = np.round(np.float128(1)-y0+delta_y) 
    i1 = np.where( y== i1_compare )[0][0]
    i2_compare = np.round(np.float128(734)-y0+delta_y)
    i2 = np.where( y==i2_compare )[0][0]
    
    #  E = E_FULL(i1:i2)
    E = E_FULL[i1:i2+1]

    #  y_out = y[i1:i2+1]
    y_out = np.linspace(1,734,734)

    return y_out,E

# Energy axis for the data of the high-gradient positron acceleration letter.
# Only for CMOS FAR camera.

# Sebastien Corde
# Create: October 15, 2014
# Last edit: October 15, 2014

# Example of usage:
# E = Energy_Axis('13450', 4.5)
# returns the energy axis E (for all CMOS FAR camera pixels, 1:2559) for
# dataset E200_13450 and for QS = 4.5 GeV.

def Energy_Axis_CMOS_FAR(dataset, QS):
    
    y  = np.linspace(1,2559,2559,dtype=np.float128)
    E0 = np.float128(20.35)

    if dataset == 13438:
        y0    = np.float128(1589)   # pixel position of E0 (20.35 GeV).
        eta_0 = np.float128(949.72) # nominal dipole dispersion in pixel, corresponding to 59.5 mm.
        
    elif dataset == 13448 or dataset == 13449:
        y0    = np.float128(1605.5) - np.float128(0.7923)*(E0+QS)  # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(949.72) + np.float128(0.7923)*(E0+QS)  # added QS dispersion of 0.7923 pix per QS GeV.
    
    elif dataset == 13450:
        y0    = np.float128(1655)   - np.float128(3.321)*(E0+QS) # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(949.72) + np.float128(3.321)*(E0+QS) # added QS dispersion of 3.321 pix per QS GeV.
        
    elif dataset == 13537:
        y0    = np.float128(1576)   + np.float(0.5193)*(20.35+QS) # y0 is adjusted to account for QS dispersion.
        eta_0 = np.float128(949.72) - np.float(0.5193)*(20.35+QS) # added QS dispersion of -0.5193 pix per QS GeV.
        
    else:
        logger.error('This dataset does not have a calibrated energy axis. Returning the nominal energy axis.')
        y0    = np.float128(1590)   # pixel position of E0 (20.35 GeV).
        eta_0 = np.float128(949.72) # nominal dipole dispersion in pixel, corresponding to 59.5 mm.
    
    E = E0 / ( np.float128(1) - (y-y0)/eta_0 )

    return y,E
