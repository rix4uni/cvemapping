OpenSSL CCS Inject Test
=======================

This script is designed for detection of vulnerable servers (CVE-2014-0224.)  in a wide range of configurations.  It attempts to negotiate using each affected protocol version (SSLv3, TLSv1, TLSv1.1, and TLSv1.2) advertising a comprehensive set of ciphers.

Changes:

v0.1 - Updated receive buffer sizes to account for longer certificate messages

v0.2 - Updated record processing to recognize closure alert when included in the same segment as another TLS record

v0.3 - Revised wording to clarify tool output and updated logic to properly recognize session termination outside of standard RFC2246 

This offline tool is not supported and is provided for informational purposes only.
This tool uses Python – license information is available here: http://opensource.org/licenses/Python-2.0
