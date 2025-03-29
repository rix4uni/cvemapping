local nmap = require "nmap"
local stdnse = require "stdnse"
local shortport = require "shortport"
local socket = require "socket"
local string = require "string"
local bit = require "bit"
local struct = require "struct"
local math = require "math"

description = [[
Detects the vulnerability in Erlang Distribution Protocol when using a default cookie value (e.g., "monster").
The script connects to the EPMD (Erlang Port Mapper Daemon) service, retrieves the node information, 
and tries to authenticate with the Erlang port using the default cookie.
]]

-- @args cookie The Erlang cookie to use for authentication (default: "monster")
-- @args epmd_port The EPMD port to use (default: 4369)
-- @args timeout Timeout for socket connections (default: 5000ms)
-- @usage
-- nmap -p 4369 --script erlang_vuln_checker --script-args cookie=monster,timeout=5000

author = "becrevex"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"vuln", "exploit"}

portrule = shortport.port_or_service(4369, "epmd", "tcp")
local function get_erlang_nodes(host, port, timeout)
    local node_list = {}
    local sock = nmap.new_socket()
    sock:set_timeout(timeout)

    local status, err = sock:connect(host, port)
    if not status then
        stdnse.print_debug(1, "Failed to connect to EPMD: %s", err)
        return nil
    end

    local cmd = "\x00\x01\x6e"
    sock:send(cmd)
    local response = sock:receive_bytes(4)
    if response == "\x00\x00\x11\x11" then
        local data = sock:receive()
        local lines = stdnse.strsplit("\n", data)
        for _, line in ipairs(lines) do
            local node_name, node_port = line:match("(.*)@.*:(%d+)")
            if node_name and node_port then
                table.insert(node_list, { name = node_name, port = tonumber(node_port) })
            end
        end
    else
        stdnse.print_debug(1, "Failed to retrieve node list from EPMD.")
        sock:close()
        return nil
    end

    sock:close()
    return node_list
end

local function authenticate_erlang_node(host, port, cookie, timeout)
    local sock = nmap.new_socket()
    sock:set_timeout(timeout)

    local status, err = sock:connect(host, port)
    if not status then
        stdnse.print_debug(1, "Failed to connect to Erlang node: %s", err)
        return false
    end

--initial NAME_MSG (\x00\x15n\x00\x07\x00\x03\x49\x9cAAAAAA@AAAAAAA)
    local name_msg = "\x00\x15n\x00\x07\x00\x03\x49\x9cAAAAAA@AAAAAAA"
    sock:send(name_msg)
    sock:receive_bytes(5) -- Receive "ok" message

    local challenge_msg = sock:receive()
    local challenge = struct.unpack(">I", challenge_msg:sub(9, 13))

    local md5_hash = nmap.md5(cookie .. challenge)
    local challenge_reply = "\x00\x15r" .. "\x01\x02\x03\x04" .. md5_hash
    sock:send(challenge_reply)
    local auth_response = sock:receive()
    sock:close()
    return #auth_response > 0
end

action = function(host, port)
    local output = {}
    local vulnerability_found = false
    local cookie = stdnse.get_script_args("cookie") or "monster"
    local epmd_port = stdnse.get_script_args("epmd_port") or 4369
    local timeout = tonumber(stdnse.get_script_args("timeout")) or 5000
    stdnse.print_debug(1, "Connecting to EPMD on port %d", epmd_port)
    local nodes = get_erlang_nodes(host, epmd_port, timeout)

    if nodes and #nodes > 0 then
        table.insert(output, "Found Erlang nodes:")
        for _, node in ipairs(nodes) do
            table.insert(output, string.format(" - %s on port %d", node.name, node.port))
            stdnse.print_debug(1, "Attempting to authenticate with node %s on port %d", node.name, node.port)
            if authenticate_erlang_node(host, node.port, cookie, timeout) then
                table.insert(output, string.format("Successfully authenticated to node %s on port %d with cookie '%s'", node.name, node.port, cookie))
                vulnerability_found = true
            else
                table.insert(output, string.format("Failed to authenticate to node %s on port %d", node.name, node.port))
            end
        end
    else
        table.insert(output, "No Erlang nodes found or failed to retrieve nodes.")
    end
    if vulnerability_found then
        return stdnse.format_output(true, table.concat(output, "\n"))
    else
        return stdnse.format_output(false, table.concat(output, "\n"))
    end
end
