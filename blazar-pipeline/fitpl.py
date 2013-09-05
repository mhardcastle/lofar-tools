#!/usr/bin/python

from matplotlib import *
from numpy import *
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

fitfunc = lambda p, x: p[0] + p[1] * x
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
powerlaw = lambda x, a, p: a*x**p

maxfile=15
cmap=cm.Set1

times = {}
if (os.path.isfile('times.txt')):
    with open('times.txt') as myfile:
        for line in myfile:
            time, var = line.partition(" ")[::2]
            times[(int)(time.strip())] = float(var)
else:
    for i in range(0,maxfile):
        times[i]=i*1.0

print times

f=open('lightcurve.txt','w')

for n in range(1,maxfile):
    sn='%1d' % n
    filename='obs'+sn+'_t_fluxes.txt.pyse'
    if (not(os.path.isfile(filename))):
        print 'skipping file',n,'it doesn\'t exist'
        continue
    lines = loadtxt(filename, unpack=False)
    mask=(lines[:,1]>0)
    med=median(lines[where(mask),1])
#    print 'median flux is',med
    mask&=(lines[:,1]>(med/2.5))
    mask&=(lines[:,1]<(med*2))
    mask&=(lines[:,0]<240)

    me=mean(lines[where(mask),2]/lines[where(mask),1])
    mask&=((lines[:,2]/lines[:,1])<(me*5.0))
    
    for iter in range(0,2):
        freq=(lines[where(mask),0]).flatten()
        flux=(lines[where(mask),1]).flatten()
        ferr=(lines[where(mask),2]).flatten()
        rows,=shape(freq)
        
        logx=log10(freq)
        logy=log10(flux)
        logyerr=ferr/(log(10)*flux)
        pinit = [1.0, -1.0]
        out = optimize.leastsq(errfunc, pinit,args=(logx, logy, logyerr), full_output=1)
        pfinal = out[0]
        index = pfinal[1]
        amp = 10.0**pfinal[0]
        covar = out[1]
        indexerr = sqrt( covar[0][0] )
        print n,iter,rows,index,indexerr,amp*225**index,mean(flux),std(flux)/sqrt(rows)
        if (iter==0):
            # clip outliers
            devs=fabs((lines[:,1]-powerlaw(lines[:,0],amp,index))/lines[:,2])
            mask&=(devs<9.0)
        else:
            plt.errorbar(freq,flux,yerr=ferr,c=cmap(n/(1.0*maxfile)),fmt='k.',label='_nolegend_')
            plt.plot(freq, powerlaw(freq, amp, index),c=cmap(n/(1.0*maxfile)),label='obs'+sn,linewidth=2)
            f.write('%10.4f %10.6f %10.6f\n' % (times[n],amp*225**index,std(flux)/sqrt(rows)))

f.close()
plt.xlabel('Frequency (MHz)')
plt.ylabel('Flux (Jy)')
plt.legend(loc=0)
plt.show()
