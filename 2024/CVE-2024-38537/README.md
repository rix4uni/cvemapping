# Detect_polyfill_CVE-2024-38537
Here's a Python script that checks if the polyfill.io domain is present in the Content Security Policy (CSP) header of a given web application.
  Steps:
  1.Save the modified script (check_csp_from_file.py) in the same directory as your urls.txt file.
  2.Run the script using python check_csp_from_file.py.
  3.The script will read each URL from urls.txt, fetch the CSP headers, and check if polyfill.io is allowed in each URL's CSP header.
