#!/usr/bin/python

# Attempt to mess with the gains using pyrap

import sys
import pyrap.tables as pt
import numpy as np
#import matplotlib.pyplot as plt

window=30

args=len(sys.argv)
if (args==1):
    print "usage: mangle_parmdb.py [instrument table]";
    sys.exit(1)

inst=sys.argv[1]
t = pt.table(inst, readonly=False, ack=False)
print t
t.summary()


names=pt.table(inst+"/NAMES", readonly=True, ack=False)
print names
names.summary()
snames=names.getcol("NAME")
print "Found",len(snames),"gain entries"
#print snames

nv=t.getcol("NAMEID")
print len(nv)

# The X co-ordinate is frequency, the Y co-ordinate time
sx=t.getcol("STARTX")
sy=t.getcol("STARTY")
ex=t.getcol("ENDX")
ey=t.getcol("ENDY")
dx=t.getkeyword('DefaultFreqStep')
dy=t.getkeyword('DefaultTimeStep')

stepx=np.rint((ex-sx)/dx);
stepy=np.rint((ey-sy)/dy);

v=t.getvarcol("VALUES")
print len(v)

for val in range(0,len(snames)):
# Don't do phase
    if (not('Amp' in snames[val])):
        print 'Skipping',snames[val]
        continue
    print snames[val]
    
    gains=[]
    times=[]
    for i in range(0,len(nv)):
        if (nv[i]==val):
            (chan, l, nm) = np.shape(v['r'+str(i+1)]);
#            print i,sx[i],sy[i],ex[i],ey[i],stepx[i],stepy[i],np.shape(v['r'+str(i+1)])
#            tm=np.array(range(0,l))
#            tm*=dy
#            tm+=(sy[i]-sy[0])
#            print len(tm),len(v['r'+str(i+1)][0,:,0])
            gains.extend(v['r'+str(i+1)][0,:,0])
#            times.extend(tm)

    print len(times),len(gains)
    if ('Amp' in snames[val]):
        gains=np.abs(gains)

    m=np.zeros(len(gains))
    for i in xrange(0,len(gains)):
        min=i-window;
        if (min<0):
            min=0;
        max=i+window;
        if (max>=len(gains)):
            max=len(gains)-1
        m[i]=np.median(gains[min:max])

#    plt.plot(times,gains)
#    plt.plot(times,m)
#    plt.xlabel("Time (s)")
#    plt.ylabel(snames[val])
#    plt.show()

# now unpack and write back

    c=0
    for i in range(0,len(nv)):
        if (nv[i]==val):
            (chan, l, num)=np.shape(v['r'+str(i+1)])
            v['r'+str(i+1)][0,:,0]=m[c:c+l];
 #           print i,sx[i],sy[i],ex[i],ey[i],stepx[i],stepy[i],np.shape(v['r'+str(i+1)])
            c+=l
 #   print 'count is',c

#t.putvarcol('VALUES',v);
for i in xrange(0,len(v)):
    t.putcol('VALUES',v['r'+str(i+1)],i,1);
