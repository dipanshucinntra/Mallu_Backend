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
print("test comment")

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get(settings.BASEURL+'/PaymentTermsTypes/$count', cookies=r.cookies, verify=False)
serPayTermsTypeCount = int(res.text)

mycursor.execute("select * from PaymentTermsTypes_paymenttermstypes")
mycursor.fetchall()
localPayTermsTypeCount = mycursor.rowcount

print(f'local Payment Terms Type count: {localPayTermsTypeCount} and server Payment Terms Type count {serPayTermsTypeCount}')
if localPayTermsTypeCount < serPayTermsTypeCount:

  res = requests.get(settings.BASEURL+'/PaymentTermsTypes', cookies=r.cookies, verify=False)
  inds = json.loads(res.text)
  for ind in inds['value']:
      print('-----Payment---')
      GroupNumber = ind['GroupNumber']
      PaymentTermsGroupName = ind['PaymentTermsGroupName']

      pytermSql = f"select * from PaymentTermsTypes_paymenttermstypes WHERE GroupNumber = '{GroupNumber}'"
      mycursor.execute(pytermSql)
      mycursor.fetchall()

      if mycursor.rowcount != 1:
        pay_sql = "INSERT INTO `PaymentTermsTypes_paymenttermstypes` (`GroupNumber`, `PaymentTermsGroupName`) VALUES ('"+str(ind['GroupNumber'])+"', '"+str(ind['PaymentTermsGroupName'])+"');"
        print(pay_sql)

        mycursor.execute(pay_sql)
        mydb.commit()
        indid = mycursor.lastrowid
        print(indid)

