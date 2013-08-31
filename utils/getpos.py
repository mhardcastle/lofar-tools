#!/usr/bin/python

import sys
import pyrap.tables as pt
import numpy as np

args=len(sys.argv)
if (args==1):
    print "usage: getpos.py [MS name]"
    sys.exit(1)

t = pt.table(sys.argv[1]+ '/OBSERVATION', readonly=False, ack=False)
name=t[0]['LOFAR_TARGET']

t = pt.table(sys.argv[1]+ '/FIELD', readonly=False, ack=False)

direction = t[0]['PHASE_DIR']
ra, dec = direction[0]

if (ra<0):
    ra+=2*np.pi;

print name[0],ra*(180/np.pi),dec*(180/np.pi)






