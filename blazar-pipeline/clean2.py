import os
import sys

root=sys.argv[4]
min=int(sys.argv[5])
max=int(sys.argv[6])
mycell=sys.argv[7]
uvmin=sys.argv[8]

print "imaging with root name",root,"between sub-bands",min,"and",max

for sb in xrange(min, max+1):
    sbn='%03d' % sb
    print 'sbn is',sbn
    myvis=root+'_SB'+sbn+'_uv.MS.dppp.flag/'
    myim='SB'+sbn
    myfits='SB'+sbn+'.fits'
    print myvis, myim, myfits
    os.system("rm -rf "+myim+".*")
    clean(imagename=myim,vis=myvis,imsize=[1024,1024],cell=mycell,selectdata=True,uvrange='>'+uvmin)
    exportfits(imagename=myim+'.image',fitsimage=myfits)
