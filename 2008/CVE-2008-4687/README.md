# CVE-2008-4687-exploit
Quick and dirty python exploit for CVE-2008-4687.

Description by NIST:
manage_proj_page.php in Mantis before 1.1.4 allows remote authenticated users to
execute arbitrary code via a sort parameter containing PHP sequences, which are 
processed by create_function within the multi_sort function in core/utility_api.php.
