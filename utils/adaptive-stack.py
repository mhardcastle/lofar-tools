#!/usr/bin/python

import numpy as np
import numpy.ma as ma
import pyfits
import sys

i=0
w=0
s=0
rms=np.zeros(len(sys.argv)-1)
for filename in sys.argv[1:]:

    fitsfile=pyfits.open(filename)
    int=fitsfile[0].data[0,0]
    mint=ma.masked_invalid(int)
    rms[i]=mint.std()
    print 'file',filename,'rms is',rms[i]
    i+=1
    fitsfile.close()

medrms=np.median(rms)
print 'median rms is',np.median(rms)

i=0
for filename in sys.argv[1:]:

    if (rms[i]<medrms*2.0 and rms[i]>medrms/6.0):
        print 'Including',filename
        fitsfile=pyfits.open(filename)
        int=fitsfile[0].data[0,0]
        fitsfile.close()
        s+=int/rms[i]
        w+=1.0/rms[i]

    i+=1

s/=w
#print s

fitsfile=pyfits.open(sys.argv[1])
fitsfile[0].data[0,0]=s
fitsfile.writeto('stack.fits',clobber=True)
fitsfile.close()
