# Usage: 
# ruby httpfuzz.rb <imagefile> <extension> <port> <fuzzfactor>
# ruby httpfuzz.rb source.gif gif 8080 30000
# https://github.com/MAVProxyUser/httpfuzz-robomiller
# based on cmiller-csw-2010.pdf Babysitting an Army of Monkeys 
# https://fuzzinginfo.files.wordpress.com/2012/05/cmiller-csw-2010.pdf

require 'webrick'
include WEBrick
require "rubygems"

if ARGV.length < 4
  puts "Too few arguments"
  puts "Usage: ruby httpfuzz.rb <imagefile> <extension> <port> <fuzzfactor>"
  exit
end

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

$pimpme = ""

REDIR_LOVE =
"<img src=\"/fuzz.#{ARGV[1]}\" ><br>fuzz</img><meta http-equiv=\"REFRESH\" content=\".5;url=/\">"
#"<iframe src=\"/fuzz.#{ARGV[1]}\" width=\"100%\" height=\"300\"></iframe>fuzz<meta http-equiv=\"REFRESH\" content=\"0;url=/\">"

File.open("index.html", 'w') {|f| f.write(REDIR_LOVE) }

s = HTTPServer.new( 
:Port => ARGV[2], 
Logger: WEBrick::Log.new("/dev/null"),
AccessLog: [],
:DocumentRoot     => "./" 

)

class REDIRECT < HTTPServlet::AbstractServlet
 def do_GET(req, res)

   res.body = REDIR_LOVE
   res['Content-Type'] = "text/html"

 end
end

class FUZZ < HTTPServlet::AbstractServlet
 def do_GET(req, res)

	testbuf = ''
	File.open(ARGV[0], "r") { |f|
	    testbuf = f.read
	}

	# Play around with this number to impact the number of writes 
	fuzzfactor = ARGV[3].to_i
#	fuzzfactor = 1000
#	fuzzfactor = 1500
#	fuzzfactor = 2000
#	fuzzfactor = 3000
#	fuzzfactor = 4000
#	fuzzfactor = 5000
#	fuzzfactor = 10000
#	fuzzfactor = 29000
#	fuzzfactor = 59000
	buflen = testbuf.length
	#puts "bufflen is #{buflen}"
	
	xFactor = (buflen.to_f / fuzzfactor).ceil
	#puts "xFactor is #{xFactor}"
	numwritesrange=(0..xFactor).to_a
	numwrites=numwritesrange.sample+1
	#puts "numwritesrange is #{numwritesrange}"

	rbyterange = (0..255).to_a
	#puts "byterange is #{rbyterange}"
	randoffsetrange = (0..(buflen-1)).to_a
	#puts "randomnumrange is #{randoffsetrange}"

	modded = ""
	numwrites.times do |i|

	        rbyte = rbyterange.sample
	        rchar = sprintf("%c", rbyte)    
	        rn = randoffsetrange.sample
	        #puts "random byte #{rn} is #{rbyte.to_s(16)}"
		
		modded = modded + "random byte #{rn} is #{rbyte.to_s(16)} "  		
	
	        testbuf[rn] = rchar
        
	end

	#puts "testbuf is now #{testbuf.to_a}"

	# ["AF_INET", 50245, "10.0.1.8", "10.0.1.8"]
	# Tue Apr 13 20:41:59 -0400 2010
	x = req.peeraddr[2] + req.request_time.to_s
	x =x.gsub(" ", "").gsub(":", "") + "." + ARGV[1]
	$pimpme = x

	puts "numwrites is #{numwrites}"
   	res.body = testbuf

	modded = modded + " numwrites is #{numwrites}"

	# Don't save the file! do so selectively 
#	File.open($pimpme, 'w') {|f| f.write(testbuf) }
 end
end

trap("INT"){ s.shutdown }
s.mount("/", REDIRECT)
s.mount("/fuzz.#{ARGV[1]}", FUZZ)

s.start


