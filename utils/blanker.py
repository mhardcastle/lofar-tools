#!/usr/bin/python

import sys, os
import numpy as np
import pyfits
import scipy.signal
import argparse

parser = argparse.ArgumentParser(description='Blanking of FITS files.')
parser.add_argument('files', metavar='FILE', nargs='+',
                   help='FITS files to process')
parser.add_argument('-z','--zero', dest='blank', action='store_const',
                   const=0, default=np.nan,
                   help='Blank with zeros instead of NaNs')
parser.add_argument('-t','--threshold', dest='threshold', action='store',
                   type=float, default=1e-5,
                   help='Threshold to use (map units)')
parser.add_argument('-n','--neighbours', dest='neighbours', action='store',
                   type=int, default=5,
                   help='Minimum number of neighbour pixels below threshold for flagging')

args = parser.parse_args()

c=0
for filename in args.files:

    fitsfile=pyfits.open(filename,mode='update')
    fitsfile.info()

    print 'Processing file ',c
    fitshdr=fitsfile[0].header

    int=fitsfile[0].data[0,0]
    
    print 'Image shape is',int.shape

    if (c>0):
        if (int.shape!=origshape):
            print "This image is a different shape from the original!"
            exit(-1)
    else:
        bad=(abs(int)<args.threshold)
        count=scipy.signal.convolve2d(bad, np.ones((3,3)), mode='same')
        mask=(count>=args.neighbours)
        origshape=int.shape

    int[np.where(mask)]=args.blank;

    c+=1
    fitsfile.flush()
    fitsfile.close()

