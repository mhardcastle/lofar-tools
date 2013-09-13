#!/usr/bin/python

# Filter a skymap file with reference to a FITS table of positions
# This version matches to FIRST sources, amalgamates sources, and
# converts all sources to points

import sys
from astropy import coordinates as coord
from astropy import units as u
from astropy.io import fits
import numpy as np

class Bunch(object):
	def __init__(self,**kwds):
		self.__dict__.update(kwds)

# open FITS table

hdulist = fits.open('/home/mjh/first-ngp.fits')
hdulist.info()
hdu=hdulist[1]
print hdu.data.shape

file = sys.argv[1]
i=0;
sources=[];
with open(file) as myfile:
        for line in myfile:
		bits=line.split(', ')
		sources.append(Bunch(counter=i,l=line,b=bits,fsn=-1,pr=0));
#		print bits
		if ((len(bits)>1) and (('POINT' in bits[1]) or ('GAUSSIAN' in bits[1]))):
			dec=bits[3]
			dec=dec.replace(".","X")
			dec=dec.replace('X',':',2)
			dec=dec.replace('X','.')
			c=coord.ICRSCoordinates(bits[2]+' '+dec,unit=(u.hour,u.degree))
			dra=np.cos(3.14159*c.dec.degrees/180)*(hdu.data.field('ra')-c.ra.degrees)
			ddec=hdu.data.field('dec')-c.dec.degrees
			dtot=np.sqrt(dra**2+ddec**2)
			fsn=np.argmin(dtot)

# does this source meet our criteria?
			min=3600*dtot[fsn]
			flux=hdu.data.field('fint')[fsn]
			if (min<10 and flux>5):

# check if an earlier (hence brighter) source has been associated with this one already
				associated=-1;
				for j in range(0,i):
					if (sources[j].fsn==fsn):
						print 'A source (',j,') is already associated with FIRST source',fsn
						associated=j;
						break;
					
# associated now holds the number of the source matched with this FIRST source

				if (associated==-1):
					sources[i].fsn=fsn
					sources[i].fflux=flux
					sources[i].lflux=(float)(bits[4])
					print bits[2],bits[3],min,flux,bits[4]
					print 'source',i,'(',bits[4],') associated with FIRST source',fsn,'(',flux,')';
				else:
					print 'adding flux of source',i,'(',bits[4],') to source',associated
					sources[associated].lflux+=(float)(bits[4])
			else:
				print 'source',i,'(',bits[4],') not associated with a FIRST source';
		else:
			sources[i].pr=1
		i+=1

outf = open('skymodel.out', 'w')

for j in range(0,i):
	if (sources[j].pr):
		outf.write(sources[j].l)
	if (sources[j].fsn>-1):
		print j,sources[j].fsn,sources[j].lflux,sources[j].fflux,'FINAL'
#		outf.write(sources[j].l)
		outf.write(sources[j].b[0]+', POINT, '+sources[j].b[2]+', '+sources[j].b[3]+(', %g, ' % sources[j].lflux)+'0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '+sources[j].b[11]+', '+sources[j].b[12])
outf.close()
