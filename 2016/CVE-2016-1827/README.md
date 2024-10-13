## flow_divert-heap-overflow

<!-- Brandon Azad -->

flow_divert-heap-overflow is a proof-of-concept exploit for [CVE-2016-1827], which was patched in
OS X El Capitan [10.11.5] and iOS [9.3.2].

[CVE-2016-1827]: https://www.cve.mitre.org/cgi-bin/cvename.cgi?name=2016-1827
[10.11.5]: https://support.apple.com/en-us/HT206567
[9.3.2]: https://support.apple.com/en-us/HT206568

The vulnerability is a series of unchecked arithmetic operations on an untrusted length supplied
from user space in the function flow_divert_handle_app_map_create. Exploitation requires root
privileges.

This proof-of-concept triggers a kernel panic OS X Yosemite 10.10.5. In El Capitan the length
fields were changed from 64 bits to 32 bits, so the message structure will need to be updated
accordingly. This exploit has not been tested on iOS.

### License

The flow_divert-heap-overflow code is released into the public domain. As a courtesy I ask that if
you reference or use any of this code you attribute it to me.
