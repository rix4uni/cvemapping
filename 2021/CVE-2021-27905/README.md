# CVE-2021-27905.POC
POC for LFI related to CVE-2021-27905

POC for [apache-solr-file-read nuclei template](https://github.com/projectdiscovery/nuclei-templates/blob/master/vulnerabilities/apache/apache-solr-file-read.yaml)

# Use 

`traverse.sh path`

For example, using /root as path, will display the content of all files (recursively) 

`> ./traverse.sh /root ` 

It's also possible to traverse and get the content of every file on the server (with reading privileges obviously) 

`> ./traverse.sh / ` 


# Documentation

The response from the vulnerable solr instance returns a `status code` the interesting values are: 

```
status: 0 -> OK 
status: 500 -> denied/forbidden. 
``` 
After that I needed to check if the response was the content of a file of a list of files and folders. To do this I just counted how many spaces the param `stream` had. Afortunately there were only 2 cases:

```
# spaces = 0  -> list of files and folders
# spaces > 0  -> content of a file. 

```

