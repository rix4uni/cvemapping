# CVE-2024-4295-Poc
CVE-2024-4295 Email Subscribers by Icegram Express &lt;= 5.7.20 - Unauthenticated SQL Injection via hash

Call Stack
```
ES_DB_Lists_Contacts->edit_subscriber_status (\email-subscribers\lite\includes\db\class-es-db-lists-contacts.php:616)
Email_Subscribers_Public->es_email_subscribe_init (\email-subscribers\lite\public\class-email-subscribers-public.php:178)
WP_Hook->apply_filters (\var\www\html\wp-includes\class-wp-hook.php:324)
WP_Hook->do_action (\var\www\html\wp-includes\class-wp-hook.php:348)
do_action (\var\www\html\wp-includes\plugin.php:517)
require_once (\var\www\html\wp-settings.php:695)
require_once (\var\www\html\wp-config.php:133)
require_once (\var\www\html\wp-load.php:50)
require (\var\www\html\wp-blog-header.php:13)
{main} (\var\www\html\index.php:17)
```
File: email-subscribers/lite/public/class-email-subscribers-public.php

![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/8bcba1a0-2e9e-475c-af31-6bb1b8cf32f5)

![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/8be9e753-a961-49c6-987b-3d611d89c7aa)

File: email-subscribers/lite/includes/db/class-es-db-lists-contacts.php

![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/8a22d75c-6669-421f-93c6-910c91d42164)

Poc:
1. Email Subscribe
![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/d19c7dec-ed65-45d9-99b2-eec242449974)

2. Check mail

![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/bb52b6b6-f8d5-4630-995b-347d677e69ed)

3. Found link format: <Host>/?es=optin&hash={{encode base64}}

Example link: 
```
http://192.168.110.184:8080/?es=optin&hash=eyJtZXNzYWdlX2lkIjowLCJjYW1wYWlnbl9pZCI6MCwiY29udGFjdF9pZCI6IjMiLCJlbWFpbCI6Imt1cDU4MjQzQGlsZWJpLmNvbSIsImd1aWQiOiJiYXNvd3otZnpjYWRqLXN6ZmxycS1qY2ViYWYtdXpxYm12IiwibGlzdF9pZHMiOlsiMiJdLCJhY3Rpb24iOiJzdWJzY3JpYmUifQ==
```

![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/999978d1-3a7a-43f2-bb6d-f76d50f40939)

Example hash: 
```
eyJtZXNzYWdlX2lkIjowLCJjYW1wYWlnbl9pZCI6MCwiY29udGFjdF9pZCI6IjMiLCJlbWFpbCI6Imt1cDU4MjQzQGlsZWJpLmNvbSIsImd1aWQiOiJiYXNvd3otZnpjYWRqLXN6ZmxycS1qY2ViYWYtdXpxYm12IiwibGlzdF9pZHMiOlsiMiJdLCJhY3Rpb24iOiJzdWJzY3JpYmUifQ==
```

Decode base64 value from parameter hash:
![image](https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/658a44be-4726-4a43-8c3c-704f81b72ca0)

https://github.com/truonghuuphuc/CVE-2024-4295-Poc/assets/20487674/c7eaae00-2da4-45c8-970c-e66b3683badc




