# WordPressMassExploiter
Mass exploiter of CVE-2015-1579 for WordPress CMS




This mass exploiter is based on CVE-2015-1579, discovered by CLAUDIO VIVIANI (https://www.exploit-db.com/exploits/36554/)


How it works:

1 - I use Selenium Framework to make the search on google.

2 - The results of search, are parsed and links are stored into wordpressAFD_results.txt file.

3 - The fuzzer() & download_wp_config() try download wp-config from all targets.


Exemple of using the tool:

$ python wordpressCVE-2015-1579.py --dork='revslider.php "index of"'

$ python wordpressCVE-2015-1579.py --dork='revslider.php "index of"' --period=lastYear (See options for this parameter on --help)


*OBS[1]: You can change the country of google search, the default is .com.br. BUT you won't be able to use --period parameter

*OBS[2]: INSTALL ALL DEPENDENCYS... (selenium beautifulsoup4 requests docopt tqdm python-nmap .... I don't remember all :D)


