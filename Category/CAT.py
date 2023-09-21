import requests, json
import time
import math
import mysql.connector

def none(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="$Bridge@2022#",
#   database="wiscon_pre"
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

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get(settings.BASEURL+'/ItemGroups/$count', cookies=r.cookies, verify=False)
servCatCont = int(res.text)

pages = math.ceil(int(res.text)/20)
print(pages)
skip=0
mycursor.execute("select * from Category_category")
mycursor.fetchall()
catCount = mycursor.rowcount

print(f'local Cat count: {catCount} and server Cat count {servCatCont}')
if catCount < servCatCont:
    for page in range(pages):

        print('in loop')

        # res = requests.get("http://122.160.67.60:50001/b1s/v1/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip="+str(skip), cookies=r.cookies, verify=False)
        
        res = requests.get(settings.BASEURL+"/ItemGroups?$select=Number,GroupName&$orderby=Number&$skip="+str(skip), cookies=r.cookies, verify=False)

        cats = json.loads(res.text)
        for cat in cats['value']:
            mycursor.execute("select * from Category_category where Number='"+str(cat['Number'])+"'")
            mycursor.fetchall()
            rc = mycursor.rowcount
            # print(rc)
            if rc != 1:
                print('-----Category---')
                GroupName = cat['GroupName'].replace("'", "''")
                print(GroupName)

                cat_sql = "INSERT INTO `Category_category` (`Number`, `GroupName`) VALUES ('"+str(cat['Number'])+"', '"+str(GroupName)+"');"
                print(cat_sql)
                mycursor.execute(cat_sql)
                mydb.commit()
                catid = mycursor.lastrowid
                print(catid)

        print('___')
        skip = skip+20
