#!/usr/bin/perl

# Pipeline for the blazar observations

use Getopt::Long;
use Term::ANSIColor;
use feature qw(switch);

chomp($cpus=`grep processor /proc/cpuinfo | wc -l`);

@steps=("Initial flagging of calibrator", "Clipping of calibrator", "BBS on calibrator", "Write out calibrator solutions", "Image calibrator", "Measure calibrator fluxes", "Initial flagging of target", "Transfer gains from calibrator", "Image target", "Measure target fluxes");
@dirs=(1,1,1,1,1,1,2,2,2,2);
@filespecs=("*.MS.dppp","*.MS.dppp.flag","*.MS.dppp.flag","*.MS.dppp.flag","*.MS.dppp.flag","SB*.fits","*.MS.dppp","*.MS.dppp.flag","*.MS.dppp.flag","SB*.fits");
$tsteps=$#steps+1;

$start=1;
$end=$tsteps;

$caldir="";
$targdir="";
$calname="3C48";
$verbose=0;
$cleanup=0;
$initonly=0;
$unpackcal="";
$unpacktarget="";
$timedep=0;

chomp($wd=`pwd`);

$result = GetOptions ("start=i" => \$start,
		      "end=i" => \$end, 
		      "cal=s" => \$caldir,
		      "target=s" => \$targdir,
		      "calname=s" => \$calname,
		      "verbose" => \$verbose,
		      "cleanup" => \$cleanup,
		      "timedep" => \$timedep,
		      "initonly" => \$initonly,
		      "unpackcal=s" => \$unpackcal,
		      "unpacktarget=s" => \$unpacktarget
    );

if ($end>$tsteps || $start<1 || $start>$end) { die("Bad start or end selected.\n"); }

if ($unpackcal) {
    if (!-d $unpackcal) { die "Directory to unpack from does not exist"};
    print color 'bold blue';
    printf("Unpack calibrator\n");
    print color 'reset';
    if (-d $caldir) {
	print color 'bold green';
	print "About to delete all contents of existing calibrator directory.\nPress return to confirm.\n";
	print color 'reset';
	$dummy=<STDIN>;
	system("rm -rf $caldir");
    }
    mkdir($caldir);
    print "Unpacking sub-bands: ";
    chomp(@files=`ls $unpackcal/*.dppp.tar`);
    chdir($caldir);
    foreach (@files) {
	system("tar xf $_");
	print '.';
    }
    print "\n";
    chdir($wd);
}

if ($unpacktarget) {
    if (!-d $unpacktarget) { die "Directory to unpack from does not exist"};
    print color 'bold blue';
    printf("Unpack target\n");
    print color 'reset';
    if (-d $targdir) {
	print color 'bold green';
	print "About to delete all contents of existing target directory.\nPress return to confirm.\n";
	print color 'reset';
	$dummy=<STDIN>;
	system("rm -rf $targdir");
    }
    mkdir($targdir);
    print "Unpacking sub-bands: ";
    chomp(@files=`ls $unpacktarget/*.dppp.tar`);
    chdir($targdir);
    foreach (@files) {
	system("tar xf $_");
	print '.';
    }
    print "\n";
    chdir($wd);
}


if (!-d $caldir) { die "Calibrator directory not specified, or does not exist"; }

if (!-d $targdir) { die "Target directory not specified, or does not exist"; }

if ($cleanup) {
    print color 'bold blue';
    printf("Cleanup phase\n");
    print color 'reset';
    chdir($wd."/".$caldir);
    chomp(@oldfiles=`ls -d * | egrep -v MS.dppp\$`);
    if ($#oldfiles>=0) {
	printf "Files to remove from calibrator dir: @oldfiles\n";
	print color 'bold green';
	print "Press return to remove them...";
	print color 'reset';
	$dummy=<STDIN>;
	system("rm -rf @oldfiles");
    } else {
	printf("No files to clean up in calibrator dir\n");
    }
    chdir($wd."/".$targdir);
    chomp(@oldfiles=`ls -d * | egrep -v MS.dppp\$`);
    if ($#oldfiles>=0) {
	printf "Files to remove from target dir: @oldfiles\n";
	print color 'bold green';
	print "Press return to remove them...";
	print color 'reset';
	$dummy=<STDIN>;
	system("rm -rf @oldfiles");
    } else {
	printf("No files to clean up in target dir\n");
    }

    chdir($wd);

}

if ($initonly) { exit; }

print color 'bold blue';
printf("Starting the pipeline: executing steps $start to $end\n");
print color 'reset';
printf("Using $cpus cores\n");

for($step=$start; $step<=$end; $step++) {
    print color 'bold green';
    printf("Step %2i: $steps[$step-1]\n",$step);
    print color 'reset';

    if ($dirs[$step-1]==1) {$dir=$caldir;}
    else {$dir=$targdir};

    chdir($wd."/".$dir);
    printf("In directory %s",`pwd`);

    chomp(@files=`ls -d $filespecs[$step-1]`);
    
    if ($#files<0) {
	print color 'bold red';
	printf("Failed to find any target files!\n");
	print color 'reset';
	exit(1);
    } else {
	printf("Working with %i files\n",$#files+1);
    }

    printf("Pre-fork step...\n") if ($verbose);

    pre_fork();

    printf("Forking to share the work...\n") if ($verbose);

    $myid=do_fork();

    printf("Greetings from the process with ID $myid\n") if ($verbose);

    $i=0;
    $logfile="log-step-".$step."-".$myid.".out";
    unlink($logfile);

    foreach $file (@files) {
	if (($i % $cpus)==$myid) {
	    in_fork();
	} 
	$i++;
    }
    
    print "Process $myid finished!\n" if ($verbose);
 
    wait_fork();

    print "\n" unless ($verbose);

    $logfile="log-step-".$step."-common.out";
    unlink($logfile);
    post_fork();
}

sub do_fork {
    my $id=0;

    for (1..$cpus-1) {

	if ($id==0) {

	    $pid=fork();
	    if (!$pid) {
		# I'm a child
		$id=$_;
	    }
	}
    }
    return $id;
}

sub wait_fork {
    if ($myid==0) {
	for (1..($cpus-1)) {
	    wait();
	}
    } else {
	exit;
    }
}    

sub pre_fork {
    printf("Here we are in the pre-fork step, $step\n") if ($verbose);
    given($step) {
	when (3) {
	    if ($timedep) {
		open INFILE, "/home/hardcastle/text/bbs-transfer-timedep.txt";
	    } else {
		open INFILE, "/home/hardcastle/text/bbs-transfer.txt";
	    }		
	    open OUTFILE, ">bbs-transfer.txt";
	    while (<INFILE>) {
		s/3C48/$calname/;
		print OUTFILE $_;
	    }
	}
	when ([6,10]) {
	    unlink("fluxes.txt");
	}
    }
}

sub in_fork {
    if ($verbose) {
	printf("Here we are in the fork step, $step, $myid, file is $file\n");
    } else {
	print '.';
    }
    given($step) {
	when ([1,7]) { 
	    system("flag_ears.py $file $myid >> $logfile 2>&1");
	};
	when (2) { 
	    system("clip.py $file >> $logfile");
	}
	when (3) {
	    system("calibrate-stand-alone -f $file bbs-transfer.txt /home/hardcastle/text/sources-calibrate.txt >> $logfile 2>&1");
	}
	when (4) {
	    $_=$file;
	    s/_uv\.MS\.dppp.flag/\.INST/;
	    $inst=$_;
	    if ($timedep) {
		$command="parmexportcal in=".$file."/instrument out=".$inst." >> $logfile 2>&1";
#		print "Command is ",$command,"\n";
		system($command);
	    } else {
		open PIPE, "|parmdbm >> $logfile 2>&1";
		print PIPE "open tablename='".$file."/instrument'\n";
		print PIPE "export Gain* tablename='$inst'\n";
		print PIPE "exit\n";
		close PIPE;
	    }
	}
#	when ([5,9]) {
#	    $file=~/.*SB(...).*/;
#	    $sb=$1;
#	    until (-f "SB".$sb.".fits") {
#		eval {
#		    local $SIG{ALRM} = sub { die "Timeout\n" };
#		    alarm 120;
#		    system("casapy --nologger --log2term -c /home/hardcastle/bin/clean-pipeline.py ".$file." ".$sb);
#		    alarm 0;
#		};
#		if ($@) {
#		    print color 'bold red';
#		    print 'Warning: CASA timed out!\n';
#		    print color reset;
#		}
#	    };
#	}
	when ([6,10]) {
	    $file=~/.*SB(...).*/;
	    $sb=$1;
	    system("dobdsm-pipeline.py $sb >> $logfile 2>&1");
	    system("pysedet.pl $file >> $logfile 2>&1");
	}
	when (8) {
	    $file=~/.*SB(...).*/;
	    chomp($inst=`ls -d $wd/$caldir/*SB$1*.INST`);
	    $call="calibrate-stand-alone -f --parmdb $inst $file /home/hardcastle/text/bbs.txt /home/hardcastle/text/sources-dummy.txt >> $logfile 2>&1";
	    system($call);
	}
    }
    
}

sub post_fork {
    printf("Here we are in the post-fork step, $step\n") if ($verbose);
    given($step) {
	when (4) {
	    print "\n";
	}
	when ([5,9]) {
	    chomp($root=`ls -d *dppp.flag | head`);
	    $root=~/^(\S+)_SA/;
	    $rootname=$1;
	    print "Executing casa clean loop with root ",$rootname,"\n";
	    system("casapy --nologger -c /home/hardcastle/bin/clean2.py ".$rootname." 0 203 >> $logfile");
	}
	when ([6,10]) { 
	    open OUTFILE, ">fluxes.txt";
	    chomp(@files=`ls *.csv`);
	    foreach $file (@files) {
		$file=~/(SB...)/;
		$bdfile=$1.".bdsm.txt";
		open INFILE, $file;
		$dummy=<INFILE>;
		$pflux=0;
		while (<INFILE>) {
		    $line=$_;
		    @bits=split(/, /,$line);
		    if ($bits[10]>$pflux) {
			$pflux=$bits[10];
			$perr=$bits[11];
		    }
		}
		close INFILE;
		if ($pflux==0) {
		    print color 'bold red';
		    print "Warning: PYSE found no sources in $file\n";
		    print color 'reset';
		    $perr=0;
		}
#		print "bdfile is $bdfile\n";
		if (!-f $bdfile) { 
		    print color 'bold red';
		    print "Warning: BDSM output file $bdfile does not exist\n";
		    print color 'reset';
		    next;
		}
		open FILE, $bdfile;
		@fluxes=();
		@errors=();
		while (<FILE>) {
		    chomp;
		    if ($_ eq "") { next; }
		    if ($_=~/ (\S+) Hz/) {
			$freq=$1/1e6;
			print OUTFILE "$freq $pflux $perr ";
			next;
		    }
		    if (/^#/) {
			next;
		    }
		    @bits=split(/\s+/);
		    push @fluxes,$bits[9];
		    push @errors,$bits[10];
		}
		@permutation=sort { $fluxes[$b] <=> $fluxes[$a] } (0..$#fluxes);
		@fluxes=@fluxes[@permutation];
		@errors=@errors[@permutation];
		printf OUTFILE "%i ",($#fluxes+1);
		for($k=0; $k<=$#fluxes; $k++) {
		    print OUTFILE "$fluxes[$k] $errors[$k] ";
		}
		print OUTFILE "\n";
		close FILE;
	    }
	    close OUTFILE;
	}
    }
}

