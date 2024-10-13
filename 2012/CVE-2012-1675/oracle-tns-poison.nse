local bin = require "bin"
local io = require "io"
local nmap = require "nmap"
local shortport = require "shortport"
local stdnse = require "stdnse"
local table = require "table"

description = [[
Simple module to test Oracle DB server for TNS Poison vulnerability.
Module sends to server a packet with command to register new TNS Listener and check response
To more details about this bug see http://seclists.org/fulldisclosure/2012/Apr/204
]]

--
-- @usage
-- nmap --script=oracle-tns-poison -p 1521 <host>
-- 
-- @output
-- PORT     STATE SERVICE REASON
-- 1521/tcp open  oracle  syn-ack
-- | oracle-tns-poison: Host is vulnerable!
--
--
-- This module is based on sid-brute script. Thanks to author: Patrik Karlsson.
--

author = "Ivan Chalykin"
license = "Same as Nmap--See http://nmap.org/book/man-legal.html"
categories = {"vuln"}

portrule = shortport.port_or_service(1521, 'oracle-tns')

local tns_type = {CONNECT=1, REFUSE=4, REDIRECT=5, RESEND=11}

local function create_tns_header(packetType, packetLength)

  local request = bin.pack( ">SSCCS",
    packetLength + 34, -- Packet Length
    0, -- Packet Checksum
    tns_type[packetType], -- Packet Type
    0, -- Reserved Byte
    0 -- Header Checksum
    )

  return request

end

local function create_connect_packet()

  local connect_data =  "(CONNECT_DATA=(COMMAND=service_register_NSGR))"

  local data = bin.pack(">SSSSSSSSSSICCA",
    308, -- Version
    300, -- Version (Compatibility)
    0, -- Service Options
    2048, -- Session Data Unit Size
    32767, -- Maximum Transmission Data Unit Size
    20376, -- NT Protocol Characteristics
    0, -- Line Turnaround Value
    1, -- Value of 1 in Hardware
    connect_data:len(), -- Length of connect data
    34, -- Offset to connect data
    0, -- Maximum Receivable Connect Data
    1, -- Connect Flags 0
    1, -- Connect Flags 1
    connect_data
    )


  local header = create_tns_header("CONNECT", connect_data:len() )

  return header .. data

end

action = function(host, port)

  local socket = nmap.new_socket()
  local catch = function() socket:close() end
  local try = nmap.new_try(catch)
  local request, response, tns_packet
  local indicator

  socket:set_timeout(2000)

      try(socket:connect(host, port))
      request = create_connect_packet( host.ip, port.number)
      try(socket:send(request))
      response = try(socket:receive_bytes(1))
 
      if response:match("ERROR_STACK") then 
        indicator="Not Vulnerable"
        else indicator="Host is vulnerable!"
        end
 
      return indicator
end
