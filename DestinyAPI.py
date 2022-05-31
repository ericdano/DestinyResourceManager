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

r = requests.post(configs['destiny_access_token_url'], data=data)
print(r.status_code)

if r.status_code == 404:
    thelogger.info('Destiny_Resource->Failed to get Access Token')
    print(r.status_code)
elif r.status_code == 200:
    thelogger.info('Destiny_Resource->Got Access Token')
    accesstoken = r.json()
    auth_token = accesstoken["access_token"]
    auth_token_header_value = "Bearer %s" % auth_token
    auth_token_header = {"Authorization": auth_token_header_value}
    #req = configs['destiny_access_base_url'] + "materials/resources/items?itemBarcode='a00007999'"
    req = configs['destiny_access_base_url'] + "materials/resources/items"
    r2 = requests.get(req, headers=auth_token_header)
    print(r2.status_code)
    #print(r2.json())
    j = r2.json()
    df = pd.DataFrame.from_dict(j)
    #results = pd.concat([pd.json_normalize(r2.json()), pd.json_normalize(r2.json(),record_path="Students", max_level=2)], axis=1).drop(columns='Students')
    #df=pd.json_normalize(r2.json(),record_path="value", max_level=1)
    #print(r2.keys())
    #json_formatted_str = json.dumps(r2, indent=1)
    #print(json_formatted_str)
    #df = pd.DataFrame[]
    print(df)