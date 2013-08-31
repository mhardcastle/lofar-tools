#!/usr/bin/python

# Read a dataset, do some statistics on the uncorrected data, and
# hence decide on flagging approach

# First argument is MS name. Second is column to filter on (DATA by
# default, could also use CORRECTED_DATA). Third is G if a global
# median filter (across all channels) should also be applied.

import sys
import pyrap.tables as pt
import numpy as np

args=len(sys.argv)
if (args==1):
    print "usage: clip.py [MS name] [column] [global?]";
    sys.exit(1)

doglobal=0
col="DATA"
ms = sys.argv[1]
if (args>2):
    col = sys.argv[2]
if (args>3):
    doglobal = (sys.argv[3]=="G")

t = pt.table(ms, readonly=False, ack=False)
data = t.getcol(col)
mask = t.getcol('FLAG')
print np.sum(mask),'flags are set'
data = np.ma.array(data, dtype=None, mask=mask)
data[np.isnan(data)]=np.ma.masked

ntime, nchan, npol = data.shape
print "Number of channels is",nchan
if (doglobal):
    OXXmed=np.ma.median(abs(data[:,:,0]));
    OYYmed=np.ma.median(abs(data[:,:,0]));
    print "Overall XX and YY medians are",OXXmed,OYYmed
for chan in xrange(nchan):
        IampXX = abs(data[:,chan,0])
        IampYY = abs(data[:,chan,3])
        XXmean=np.ma.mean(IampXX)
        YYmean=np.ma.mean(IampYY)
        XXmed=np.ma.median(IampXX)
        YYmed=np.ma.median(IampYY)
        
        print "Channel ",chan,"XX Mean ",XXmean, 'XX Median', XXmed
        print "           YY Mean ",YYmean, 'YY Median', YYmed

        filter=(IampXX>XXmed*3);
        print "Filter removes ",np.sum(filter),"XX points"
        mask[:,chan,0]|=filter
        filter=(IampYY>YYmed*3);
        print "Filter removes ",np.sum(filter),"YY points"
        mask[:,chan,3]|=filter

        if (doglobal):
            filter=(IampXX>OXXmed*5);
            print "Global filter removes ",np.sum(filter),"XX points"
            mask[:,chan,0]|=filter
            filter=(IampYY>OYYmed*5);
            print "Global filter removes ",np.sum(filter),"YY points"
            mask[:,chan,3]|=filter

print np.sum(mask),'flags are set'
print "Writing back to table!"
t.putcol('FLAG',mask)
