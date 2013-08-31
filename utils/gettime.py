#!/usr/bin/python

import sys
import pyrap.tables as pt
import numpy as np
from astropy.time import Time

args=len(sys.argv)
if (args==1):
    print "usage: gettime.py [MS name]"
    sys.exit(1)

t = pt.table(sys.argv[1]+ '/OBSERVATION', readonly=False, ack=False)
name=t[0]['LOFAR_TARGET']

(start,end)=t[0]['TIME_RANGE']/86400.0

tstart=Time(start, scale='utc', format='mjd')
tend=Time(end, scale='utc', format='mjd')

print name[0],start,end,(start+end)/2.0
print '     ',tstart.iso,tend.iso






