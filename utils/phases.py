#!/usr/bin/python

# Attempt to dump out the station gains and plot them
# Basic structure stolen from ~swinbank/edit-parmdb/edit_parmdb.py

import sys
import numpy
from parmdb.stationgain import StationGain
from parmdb.utils import list_stations
import matplotlib.pyplot as plt

args=len(sys.argv)
if (args==1):
    print "usage: gains.py [instrument table] [substring]";
    sys.exit(1)

filename=sys.argv[1]
stations = list_stations(filename)
print 'Stations are',stations

for station in stations:
        print "Processing station",station
	if (station[1]!="S"):
# Deals with case where we have rotation for a source, in which case
# it appears to this code as a station; only things with names that
# look like stations should be used here.
		continue
	if ((args==3) and not(sys.argv[2] in station)):
		continue
        sgain=StationGain(filename, station)
        for pol, data in sgain.iteritems():
            if (pol == "0:0" or pol == "1:1"):
                if (pol == "0:0"):
                    ls="r-"
                else:
                    ls="b-"
                phases = data.phase
                timescale = sgain.timescale - sgain.timescale[0]
                print pol,numpy.mean(phases)
                plt.plot(timescale,phases,ls)

plt.xlabel("Time (s)")
plt.ylabel("Gain phase (radians)")
#plt.axis([0,120,0,0.2])
plt.show()
