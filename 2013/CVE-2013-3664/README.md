Sketchup MAC Pict Material Palette Stack Corruption - CVE-2013-3664
===================================================================

SketchUp fails to validate the input when parsing an embedded MACPict texture. Arbitrary code execution is proved possible after a malicious texture or thumbnail or background image triggers a stack overflow.  The issue can also be triggered when Windows Explorer reads the embedded thumbnail in a .skp file.

Summary
=======
* Title: Sketchup MAC Pict Material Palette Stack Corruption
* CVE ID: CVE-2013-3664
* Permalink: http://www.binamuse.com/advisories/BINA-20130521A.txt
* Advisory Published: 2013-05-23
* Class: Boundary Error Condition (Buffer Overflow)
