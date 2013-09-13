#!/usr/bin/python

import sys
from astropy.io import fits

h1=fits.open(sys.argv[1])
h2=fits.open(sys.argv[2])

r=h1[0].data[0,0]-h2[0].data[0,0]

h1[0].data[0,0]=r

h1.writeto('diff.fits',clobber=True)
