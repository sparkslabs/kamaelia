#!/usr/bin/perl

opendir(IN, 'Support/wav') ||die "$!?";
while($A = readdir(IN)) {
   next if ($A =~ /^\.\.?$/);
   push @dir, $A;
}
closedir IN;
$file = $dir[rand(scalar @dir)];
open(IN, "Support/wav/$file");
while($A=<IN>) {
   print $A
}
close IN;

