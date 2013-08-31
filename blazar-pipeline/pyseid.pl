#!/usr/bin/perl

# Get the central RA and DEC

chomp($ms=`ls -d *.dppp | head -1`);

$pos=`getpos.py $ms`;
$pos=~/(\S+) (\S+) (\S+)/;
$cra=$2;
$cdec=$3;

$count=0;
$tolerance=0.03;
foreach (@ARGV) {
    $file=$_;
    $i=0;
#    print "File $count:\n";
    die("File $file does not exist") if (!-f $file);
    open INFILE,$file;
    $dummy=<INFILE>;
    while (<INFILE>) {
	chomp;
	@bits=split(/, /);
	$ra[$count][$i]=$bits[0];
	$dec[$count][$i]=$bits[2];
	$flux[$count][$i]=$bits[12];
	$ferr[$count][$i]=$bits[13];
#	printf "%i %f %f %f %f\n",$i,$ra[$count][$i],$dec[$count][$i],$flux[$count][$i],$ferr[$count][$i];
	$i++;
    }
    close INFILE;
    $num[$count]=$i;
    $file=~s/csv/fits/;
    chomp($fname[$count]=`getfrq-image.py $file`);
    $count++;
}

# Compute distances for first set of positions

for($j=0; $j<$num[0]; $j++) {
    $cdist[$j]=sqrt(($ra[0][$j]-$cra)**2.0+($dec[0][$j]-$cdec)**2.0);
}

@ranks[sort { $cdist[$a] <=> $cdist[$b] } 0 .. $num[0]-1] = 0 .. $num[0]-1;

open OUTFILE,">sourcelookup.txt";

for($j=0; $j<$num[0]; $j++) {
    printf OUTFILE "%2i %10.6f %10.6f %6.3f %6.3f %2i\n",$j,$ra[0][$j],$dec[0][$j],$flux[0][$j],$ferr[0][$j],$ranks[$j];
}
close OUTFILE;

#print "Cross-matching\n";

for($i=1; $i<$count; $i++) {
#    print "Cross-matching file $i\n";
    for($j=0; $j<$num[0]; $j++) {
	$matchflux[$j][$i]=0;
	$matchferr[$j][$i]=0;
	for($k=0; $k<$num[$i]; $k++) {
	    $dist=sqrt(($ra[0][$j]-$ra[$i][$k])**2.0+($dec[0][$j]-$dec[$i][$k])**2.0);
	    if ($dist<$tolerance) {
#		print "Matched source $j with source $k ($flux[0][$j], $flux[$i][$k])\n";
		$matchflux[$j][$i]=$flux[$i][$k];
		$matchferr[$j][$i]=$ferr[$i][$k];
	    }
	}
    }
}

for($j=0; $j<$num[0]; $j++) {
    open OUTFILE,">fluxes-$ranks[$j].txt";
    for($i=1; $i<$count; $i++) {
	$aveflux[$j]+=$matchflux[$j][$i];
	print OUTFILE $fname[$i]," ",$matchflux[$j][$i]," ",$matchferr[$j][$i],"\n";
    }
    close OUTFILE;
}
