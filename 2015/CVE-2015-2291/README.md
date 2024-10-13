# Intel-CVE-2015-2291
PoC exploit for CVE-2015-2291

Data-only attack to pop a system shell with the vulnerable intel driver.

The code itselfs implements more "functionality" provided from the driver, like physical to virtual address translation, mapping physical memory (This two combined  = arbitrary kernel memory overwrite) so it can be used to execute arbitrary code in the kernel.


