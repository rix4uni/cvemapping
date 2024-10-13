# CVE-2017-15394

>A URL spoofing flaw has been found in the extensions UI of the Chromium browser < 62.0.3202.62.

An IDN homograph attack demo in Chromium through extensions.

1) Load unpacked extension into Chrome
2) View extension details and observe lack of punycode

## Impact

An attacker would leverage this weakness to aid in deception attacks by coercing a victim into granting the extension permissions to an unexpected domain.

## Patch

Released October 17, 2017: <https://chromereleases.googleblog.com/2017/10/stable-channel-update-for-desktop.html>