#!/usr/bin/python

import sys, os
import numpy as np
import pyfits
import scipy.signal

threshold=1e-5;

for filename in sys.argv[1:]:

    fitsfile=pyfits.open(filename,mode='update')
    fitsfile.info()

    fitshdr=fitsfile[0].header

    int=fitsfile[0].data[0,0]
    
    print 'Image shape is',int.shape
    
    bad=(abs(int)<threshold)
    count=scipy.signal.convolve2d(bad, np.ones((3,3)), mode='same')
    mask=(count>=5)

    int[np.where(mask)]=np.nan;

    fitsfile.flush()

