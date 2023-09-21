import requests, json
import time
import math
import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Sunil@123",
#   database="vision_web"
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

mycursor = mydb.cursor()
print("test comment")

# with open("../bridge/db1.json") as f:

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get(settings.BASEURL+'/Departments', cookies=r.cookies, verify=False)

bps = json.loads(res.text)
print(len(bps['value']))
for bp in bps['value']:
    print('-----Position---')
    print(bp['Code'])
    print(bp['Name'])
    print(bp['Description'])
    
    dep_sql = "INSERT INTO `BusinessPartner_bpdepartment` (`Code`, `Name`, `Description`) VALUES ('"+str(bp['Code'])+"', '"+str(bp['Name'])+"', '"+str(bp['Description'])+"');"

    mycursor.execute(dep_sql)
    mydb.commit()
    #print(mycursor.last_inserted_id())
