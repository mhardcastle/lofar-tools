#!/usr/bin/python

import sys
import pyrap.tables as pt

args=len(sys.argv)
if (args==1):
    print "usage: getfreq.py [MS name]"
    sys.exit(1)

t = pt.table(sys.argv[1]+ '/OBSERVATION', readonly=False, ack=False)
name=t[0]['LOFAR_TARGET']

t = pt.table(sys.argv[1]+ '/SPECTRAL_WINDOW', readonly=False, ack=False)

freq = t[0]['REF_FREQUENCY']
channels = t[0]['NUM_CHAN']
chlist=t[0]['CHAN_FREQ']

print name[0],freq/1e6,'MHz',channels,chlist









