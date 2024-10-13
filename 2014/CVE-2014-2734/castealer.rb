#!/usr/bin/env ruby

require 'openssl'

key = OpenSSL::PKey::RSA.new(2048)
ca_cert = OpenSSL::X509::Certificate.new(File.read("ca.pem"))

puts "before we sign the cert: #{ca_cert.verify(key)}"
ca_cert.sign(key, OpenSSL::Digest::SHA1.new)
puts "after we sign the cert: #{ca_cert.verify(key)}"
