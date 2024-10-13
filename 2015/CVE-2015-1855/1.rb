require 'openssl'

raw = File.read "sub.example.org.pem" # DER- or PEM-encoded
certificate = OpenSSL::X509::Certificate.new raw
puts OpenSSL::SSL.verify_certificate_identity(certificate,"sss.xxx.sub.example.org")
