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

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sunil@123",
  database="vision_test"
)
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
    with open("/home/www/cinntra/vision_test/bridge/bridge/db.json") as f:
            
            

        
    r = requests.post('http://103.107.67.93:50001/b1s/v1/Login', data=json.dumps(settings.SAPDB), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)
    
    addr = "http://103.107.67.93:50001/b1s/v1/Orders?$select=DocEntry,DocumentStatus&$filter=(DocumentStatus eq 'bost_Close') and "
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
    
        #mycursor.execute(sql)
        #mydb.commit()
    #itemid = mycursor.lastrowid
    #print(itemid)
