#!/usr/bin/python

# Filter a skymap file with reference to a FITS table of positions

import sys
from astropy import coordinates as coord
from astropy import units as u
from astropy.io import fits
import numpy as np

# open FITS table

hdulist = fits.open('/home/mjh/first-ngp.fits')
hdulist.info()
hdu=hdulist[1]
print hdu.data.shape

outf = open('skymodel.out', 'w')
file = sys.argv[1]
with open(file) as myfile:
        for line in myfile:
		bits=line.split(', ')
#            print bits
		if ('hires' in bits[0]):
			bits[3]=bits[3].replace(".","X")
			bits[3]=bits[3].replace('X',':',2)
			bits[3]=bits[3].replace('X','.')
			c=coord.ICRSCoordinates(bits[2]+' '+bits[3],unit=(u.hour,u.degree))
			dra=np.cos(3.14159*c.dec.degrees/180)*(hdu.data.field('ra')-c.ra.degrees)
			ddec=hdu.data.field('dec')-c.dec.degrees
			dtot=np.sqrt(dra**2+ddec**2)
			i=np.argmin(dtot)
			min=3600*dtot[i]
			flux=hdu.data.field('fint')[i]
			if (min<10 and flux>10):
				print bits[2],bits[3],min,flux,bits[4]
				outf.write(line)
		else:
			outf.write(line)
outf.close()
