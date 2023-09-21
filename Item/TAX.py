import requests, json
import time
import math
import mysql.connector

def none(inp):
	if type(inp)!=float:
		return 0;
	else:
		return inp


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
# print("test comment")

# with open("../bridge/db_web.json") as f:
    

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
# print(token)

res = requests.get(settings.BASEURL+'/SalesTaxCodes', cookies=r.cookies, verify=False)

taxs = json.loads(res.text)

for tax in taxs['value']:
    print('-----Tax---')
    print(tax['Name'])
    print(tax['Rate'])
    print(tax['Code'])
    
    print("select Code from Item_tax where Code='"+str(tax['Code'])+"'")
    mycursor.execute("select * from Item_tax where Code='"+str(tax['Code'])+"'")
    mycursor.fetchall()
    rc = mycursor.rowcount
    print(rc)
    if rc != 1:
        tax_sql = "INSERT INTO `Item_tax` (`Rate`, `Code`, `Name`) VALUES ('"+str(none(tax['Rate']))+"', '"+str(tax['Code'])+"', '"+str(tax['Name'])+"');"
        print(tax_sql)
        mycursor.execute(tax_sql)
        mydb.commit()
    #taxid = mycursor.lastrowid
    #print(taxid)
