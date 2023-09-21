import requests, json
import time
import math
import mysql.connector

from pytz import timezone
from datetime import datetime as dt
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')
print(date)
print(time)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="$Bridge@2022#",
#   database="vision_dev"
# )

#--- start dynamic-----
import sys, os
dir = os.getcwd()
dir = dir.split("/bridge/")[0]+"/bridge"
sys.path.append(dir)
from bridge import settings

mydb = mysql.connector.connect(
  host=settings.DATABASES['default']['HOST'],
  user=settings.DATABASES['default']['USER'],
  password=settings.DATABASES['default']['PASSWORD'],
  database=settings.DATABASES['default']['NAME']
)

#----end dynamic---

mycursor = mydb.cursor(dictionary=True)
print("test comment")

print("SELECT DocEntry FROM `Order_order` WHERE `DocumentStatus` 'bost_Open'")
mycursor.execute("SELECT DocEntry FROM `Order_order` WHERE `DocumentStatus` = 'bost_Open'")
obj = mycursor.fetchall()
rrc = mycursor.rowcount
print(rrc)
if rrc != 0:
    sql=[]
    for rc in obj:
        num = str(rc['DocEntry'])
        sql.append("DocEntry eq "+str(num))
    param = " or ".join(sql)
    print(param)
    # with open("/home/www/b2b/vision_dev/bridge/bridge/db.json") as f:
            
 
    r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)
    
    # addr = "http://122.160.67.60:50001/b1s/v1/Orders?$select=DocEntry,DocumentStatus&$filter=(DocumentStatus eq 'bost_Close') and "
    addr = settings.BASEURL+"/Orders?$select=DocEntry,DocumentStatus&$filter=(DocumentStatus eq 'bost_Close') and "
    url = addr+"("+param+")"
    print(url)
    res = requests.get(url, cookies=r.cookies, verify=False)
    live = json.loads(res.text)
    print(live)
    if len(live['value']) > 0:
        for doc in live['value']:
            print(doc['DocEntry'])
            print(doc['DocumentStatus'])
            mycursor.execute("UPDATE `Order_order` SET `DocumentStatus` = 'bost_Close' WHERE `DocEntry` = "+str(doc['DocEntry'])+";")
            mydb.commit()
