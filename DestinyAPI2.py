import pandas as pd
import requests, json, logging, smtplib, datetime
from pathlib import Path
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from logging.handlers import SysLogHandler


#load configs
home = Path.home() / ".DestinyResource" / "DestinyResource.json"
confighome = Path.home() / ".DestinyResource" / "DestinyResource.json"
with open(confighome) as f:
  configs = json.load(f)
# Logging to a log server
if configs['logserveraddress'] is None:
    logfilename = Path.home() / ".DestinyResource" / configs['logfilename']
    thelogger = logging.getLogger('MyLogger')
    thelogger.basicConfig(filename=str(logfilename), level=thelogger.info)
else:
    thelogger = logging.getLogger('MyLogger')
    thelogger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = (configs['logserveraddress'],514))
    thelogger.addHandler(handler)

data = {
    "grant_type": configs['grant_type'],
    "client_id": configs['client_id'],
    "client_secret": configs['client_secret']
}

destiny_endpoint_url = ""


#print(r.status_code)
def get_token():
    r = requests.post(configs['destiny_access_token_url'], data=data)
    if r.status_code == 200:
        thelogger.info('Destiny_Resource->Got Access Token')
    else:
        print(r.status_code)
    return r.json()

def main_request(baseurl, endpoint, token):
    r2 = requests.get(baseurl + endpoint, headers=auth_token_header)
    if r2.status_code == 200:
        thelogger.info('Destiny_Resource->Got GET request')
    else:
        print(r2.status_code)
    return r2.json()

#def get_pages(response):


thelogger.info('Destiny_Resource->Got Access Token')
accesstoken = get_token()
auth_token = accesstoken["access_token"]
auth_token_header_value = "Bearer %s" % auth_token
auth_token_header = {"Authorization": auth_token_header_value}
#req = configs['destiny_access_base_url'] + "materials/resources/items?itemBarcode='a00007999'"
#r2 = requests.get(req, headers=auth_token_header, params=[('itemBarcode','a00007999')])
destiny_endpoint_url =  "materials/resources/items"
#req = configs['destiny_access_base_url'] + destiny_endpoint_url
j = main_request(configs['destiny_access_base_url'],destiny_endpoint_url,auth_token_header)
#r2 = requests.get(req, headers=auth_token_header)
#print(r2.status_code)
#print(r2.json())
#    print('-----------')
#    print(type(r2))
#j = r2.json()
print(json.dumps(j,indent=2))
for i in j['value']:
    serialnum = i['serialNumber']
    barcode = i['barcode']
    resourcet = i['resource']['name']
    for a in i['itemFields']:
        print(str(a['name']) + "-" + str(a['value']))
    print(barcode)
    print(serialnum)
    print(resourcet)
print(j['@nextLink'])
