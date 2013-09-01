#!/usr/bin/perl

foreach (`ls -d obs*_t`) {
    chomp;
    $dir=$_;
    chomp($vis=`ls -d $dir/vis-SB*ms | head -n 1`);
    $line=`gettime.py $vis`;
    @bits=split(/\s+/,$line);
    $dir=~/obs(\S+)_t/;
    $number=$1;
    print $1," ",$bits[3],"\n";
}
