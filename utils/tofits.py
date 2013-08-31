#!/usr/bin/python

# Write CASA image to fits

import sys
import pyrap.images as pi
import os.path

args=len(sys.argv)
if (args==1):
    print "usage: tofits.py [CASA images]";
    sys.exit(1)

for fn in sys.argv[1:]:
    print 'Doing',fn
    outname=fn+'.fits'
    if os.path.isfile(outname):
        print '... skip, FITS file already exists'
        continue

    im=pi.image(fn)
    im.tofits(outname)
    print '... writing FITS file'
