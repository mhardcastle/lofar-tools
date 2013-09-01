#!/usr/bin/perl

# Testing the use of the detimage variant of pyse

if (-d"/home/swinbank") {
    $PYSE_PATH="/home/swinbank/pyse-detimage";
    $ENV{'LD_LIBRARY_PATH'}=$PYSE_PATH."/lib:".$ENV{'LD_LIBRARY_PATH'};
    $ENV{'PYTHONPATH'}=$PYSE_PATH."/lib/python2.6/site-packages:".$ENV{'PYTHONPATH'};
    $pyse=$PYSE_PATH."/bin/pyse.py";
} else {
    $pyse="pyse.py";
}

foreach(@ARGV) {
    $file=$_;

    if ($file eq "stack.fits") {
	system($pyse." --margin=10 --csv --force-beam ".$file);
    } else {
	system($pyse." --margin=10 --detection-image=stack.fits --csv --force-beam ".$file);
    }
}
