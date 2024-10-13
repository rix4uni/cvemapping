#!/usr/bin/env ruby

require 'webrick'
require 'logger'

$stdout = IO.new(IO.sysopen("/proc/1/fd/1", "w"),"w")
$stdout.sync = true
STDOUT = $stdout
logger = Logger.new(STDOUT)

server = WEBrick::HTTPServer.new(
  :Port => 80,
)

server.mount_proc '/' do |req, res|
  logger.debug(req.path)
  logger.debug(req.raw_header)
  logger.debug(req.body)
  res.body = 'hello world'
end

server.mount_proc '/flag' do |req, res|
  logger.debug(req.path)
  logger.debug(req.raw_header)
  logger.debug(req.body)
  res.body = 'flag is 123456'
end

server.start
