import requests, json
import time
import math
import mysql.connector

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

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get(settings.BASEURL+'/Industries/$count', cookies=r.cookies, verify=False)
serIndustriesCount = int(res.text)

mycursor.execute("select * from Industries_industries")
mycursor.fetchall()
localIndustriesCount = mycursor.rowcount


print(f'local Industires count: {localIndustriesCount} and server Industires count {serIndustriesCount}')
if localIndustriesCount < serIndustriesCount:

   res = requests.get(settings.BASEURL+'/Industries', cookies=r.cookies, verify=False)
   inds = json.loads(res.text)

   for ind in inds['value']:
      
      print('-----SalePersons---')
      IndustryDescription = ind['IndustryDescription']
      IndustryName = ind['IndustryName']
      IndustryCode = ind['IndustryCode']

      inds_sql = f"select * from `Industries_industries` WHERE IndustryCode={IndustryCode}"
      print(inds_sql)
      mycursor.execute(inds_sql)
      mycursor.fetchall()
      if mycursor.rowcount != 1:

         ind_sql = f"INSERT INTO `Industries_industries` (`IndustryDescription`, `IndustryName`, `IndustryCode`) VALUES ('{IndustryDescription}', '{IndustryName}', '{IndustryCode}')"
         print(ind_sql)

         mycursor.execute(ind_sql)
         mydb.commit()
         indid = mycursor.lastrowid
         print(indid)
