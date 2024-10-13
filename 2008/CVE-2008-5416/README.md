# CVE-2008-5416

Microsoft SQL Server sp_replwritetovarbin Memory Corruption via SQL Injection

A heap-based buffer overflow can occur when calling the undocumented
"sp_replwritetovarbin" extended stored procedure. This vulnerability affects
all versions of Microsoft SQL Server 2000 and 2005, Windows Internal Database,
and Microsoft Desktop Engine (MSDE) without the updates supplied in MS09-004.
Microsoft patched this vulnerability in SP3 for 2005 without any public
mention.

Credits:

          'jduck',          # MS09-004 base exploit
          'Rodrigo Marcos'  # SQL Injection mods
