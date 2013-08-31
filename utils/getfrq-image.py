#!/usr/bin/python

import pyfits
import sys

filename=sys.argv[1]
fitsfile=pyfits.open(filename)
print fitsfile[0].header['restfrq']/1.0e6

