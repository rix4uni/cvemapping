# CVE-2024-30956
cf https://www.lauyan.com/en/toweb-updates.html#iyFEw37D

(DOM-based XSS) HTML Injection vulnerability in TOWeb version 5 <= 12.05 allows an attacker to inject HTML/JS code via the `_message.html` component.

## Explanation
- the `_message.html` file is used to display an error page, by decoding and executing the cypher right to the `?`.
- the cypher is HTML code, base64 encoded, then reversed (for an english website, the error page would be `127.0.0.1:8000/_message.html?==gP2lGZvwjP2lGZvwjPyJGP+InY84DcvwDZuV3bGBCdv5EIldWYQ5Dc84jMo9CPg4jMoxjPiEmchBXL3RnI9M3chx2YgYXakxjPxg2L8IXdlJncF5TMoxjPiIXZ05WZjpjbnlGbh1Cd4VGdi0TZslHdzBidpRGP`)
- since this is HTML code, we can add javascript code in it, that will be executed when the user navigates to the url

## Impact
- For instance, XSS can be used with social engineering to steal user credentials or trick a user into downloading a malware, using a user's trust in a company against them.
- cf https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#exploit-code-or-poc

## Mitigation
- This vulnerability is fixed in version 12.06

# Exploit
- `python3 poc.py; python3 -m http.server -d src` -> eg http://127.0.0.1:8000/_message.html?==gC+QHcpJ3Yz9CPpcyUThFIkV2chJWLN9ERngCdyVGbh5DdwlmcjNHP
- navigate to the url, the JS code is executed
- PS: src contains a copy of the relevant HTML/JS code, since TOWeb is closed source and doesn't allow to download an older version without paying
