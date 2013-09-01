import os
import sys

sb=(int)(sys.argv[6])
myvis=sys.argv[5]

print "imaging ms ",myvis," sub-band number ",sb;

sbn='%03d' % sb
print 'sbn is',sbn
myim='SB'+sbn
myfits='SB'+sbn+'.fits'
print myvis, myim, myfits
os.system("rm -r "+myim+".*")
clean(imagename=myim,vis=myvis,imsize=[1024,1024],cell='15')
exportfits(imagename=myim+'.image',fitsimage=myfits)
