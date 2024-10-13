# rtf_exploit_extractor
Script to extract malicious payload and decoy document from CVE-2015-1641 exploit documents

	usage: rtfexploit_extract.py [-h] [-o OUTFILE] [-d DECOY] [-l LENGTH] [-v] inputfile
	
	
	inputfile             exploit document to examine
	
	optional arguments:
	
		-h, --help			show this help message and exit
	  
	  	-o OUTFILE, --outfile OUTFILE
	  						output filename for extracted payload
	  						
		-d DECOY, --decoy DECOY
							output filename for extracted decoy document
							
	  	-l LENGTH, --length LENGTH
							length of each marker to search for (def: 7)
							
		-v                    print debug messages


All args are optional except for input filename.

Ref: http://blog.malwareclipboard.com/2015/10/rtf-exploit-document-extraction.html
