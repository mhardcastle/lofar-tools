#!/usr/bin/python

import numpy as np
import pyfits
import sys

i=0
w=0
s=0
for filename in sys.argv[1:]:

    fitsfile=pyfits.open(filename)
    int=fitsfile[0].data[0,0]
    rms=int.std()
    print 'file',filename,'rms is',rms

    if (rms<1.5):
        s+=int/rms
        w+=1.0/rms
    else:
        print '... rejecting from stack'

s/=w
print s

fitsfile[0].data[0,0]=s
fitsfile.writeto('stack.fits',clobber=True)
