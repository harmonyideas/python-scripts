#!/usr/local/bin/perl

##
#VERSION: 1.0 MODIFIED: 2 / 12 / 11
# DESCRIPTION: Search Fortinet Config File by Object Reference­ Global Matches are# Supported(ex. "config vpn ipsec" or "config vpn ipsec phase1­interface")
##

use strict;
if ($# ARGV != 1) {
    print "usage: test.pl <config file> \"<config object>\" \n";
    exit;
}
my $configFile = $ARGV[0];
my $configObject = $ARGV[1];
my $sectionEnd = "end";
my $endTag = "end\n";
my $line = "";
my $string = "";
#escape harmful characters
for regex
$configObject = ~/\Q$configObject\E/;
#allow
for reading entire file into string
local $ / = undef;
# open config file
open(OF, $configFile) or die "Can't open $configFile : $!";#
loop each line searching
for start / end tags
while ($line = < OF > ) {
    while ($line = ~
        /$configObject(.*?)\b$sectionEnd\b/sg)
        # /s . cross line boundaries {
        # quit if we reach end of file
        close OF
        if eof;
        # add start and end tags to config section
        $string = $string.$configObject.$1.$endTag;
    }
}
close(OF);# remove leading whitespace and print string
$string = ~s / \h + / /g;
printf($string);
