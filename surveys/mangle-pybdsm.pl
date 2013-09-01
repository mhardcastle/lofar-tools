#!/usr/bin/perl

# Mangle pybdsm output along the lines used for MSSS work

$smname=shift(@ARGV);
$outname="selfcal.model";
$ptthresh=200;
$fluxthresh=0.2;

print "Will generate sky model $outname\n";

open INFILE, $smname or die "Can't open $smname";
open OUTFILE, ">$outname";
# copy header line
$line=<INFILE>;
print OUTFILE $line;
$line=<INFILE>;
$count=0;
$convert=0;
while (<INFILE>) {
    chomp;
    @bits=split(/, /);
#	print("Contemplating source $bits[0]...\n");
    if ($bits[4]>$fluxthresh) {
	$count++;
#	print $bits[1],$bits[8],"\n";
	if (($bits[1] eq "GAUSSIAN") && ($bits[8]<$ptthresh)) {
	    $bits[1]="POINT";
	    $bits[8]="0.0";
	    $bits[9]="0.0";
	    $bits[10]="0.0";
	    $convert++;
	}
	for($i=0; $i<=$#bits; $i++) {
	    print OUTFILE ", " if ($i);
	    print OUTFILE $bits[$i];
	}
	print OUTFILE "\n";
    }
}
close INFILE;
close OUTFILE;

print "$count sources in sky model ($convert converted from Gaussians to points)\n";
die("No sources in sky model, something is wrong!") if (!$count);
