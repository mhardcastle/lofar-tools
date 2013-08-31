import os
import sys

min=int(sys.argv[4])
max=int(sys.argv[5])
mycell=sys.argv[6]
uvmin=sys.argv[7]

print "imaging between sub-bands",min,"and",max

for sb in xrange(min, max+1):
    sbn='%03d' % sb
    print 'sbn is',sbn
    myvis='vis-SB'+sbn+'.copy.ms'
    myim='SB'+sbn
    myfits='SB'+sbn+'.fits'
    print myvis, myim, myfits
    os.system("rm -rf "+myim+".*")
    clean(imagename=myim,vis=myvis,imsize=[1024,1024],cell=mycell,selectdata=True,uvrange='>'+uvmin)
    exportfits(imagename=myim+'.image',fitsimage=myfits)
