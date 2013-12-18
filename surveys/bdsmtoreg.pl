#!/usr/bin/perl

# Convert pybdsm BBS-format output to a ds9 region file for ease of visualization

$color="green";

$infile=shift(@ARGV);
$outreg=shift(@ARGV);

open(INFILE,$infile) or die("Can't open input file");
open(OUTREG,">$outreg") or die("Can't open output file");

print OUTREG "# Region file format: DS9 version 4.1\nglobal color=$color dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n";

while (<INFILE>) {
    chomp;
    if (/^#/ or $_ eq "") {
	next;
    }
    @bits=split(/, /);
    $ra=$bits[2];
    @decbits=split(/\./,$bits[3]);
    $dec=$decbits[0].":".$decbits[1].":".$decbits[2].".".$decbits[3];
    $flux=$bits[4];
    $maj=$bits[8];
    $min=$bits[9];
    $pa=$bits[10];
    print "$bits[1] $ra $dec $bits[4]\n";
    if ($bits[1] eq "POINT") {
	print OUTREG "point($ra,$dec) # point=cross\n";
    } else {
	printf OUTREG "ellipse($ra,$dec,%.3f\",%.3f\",%.3f)\n",$maj,$min,$pa; 
    }
}

