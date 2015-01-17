import E200
import numpy as np

__all__ = ['laser_on_off']

def laser_on_off(imgstr,uid):
    #  data = E200.E200_load_data('nas/nas-li20-pm00/E200/2014/20140629/E200_13537',local=True)
    
    #  imgstr = data.rdrill.data.raw.images.E224_Probe._hdf5
    #  uid = data.rdrill.data.raw.images.E224_Probe.UID
    
    out = E200.E200_load_images(imgstr,uid)
    
    num_imgs = len(out.images)
    
    lasercount = np.zeros(num_imgs,dtype=np.int64)
    laseron    = np.zeros(num_imgs,dtype=np.int)
    switch = np.ones(num_imgs-1,dtype=np.int)
    
    for i,val in enumerate(out.images):
        lasercount[i] = np.sum(val)
    
    laseron[lasercount > 2e7] = np.int(True)
    
    for i,val in enumerate(switch):
        if laseron[i+1] == laseron[i]:
            switch[i] = False
    
    #  data.close()

    return laseron
