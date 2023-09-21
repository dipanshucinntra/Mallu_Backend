import requests, json
import time
import math
import mysql.connector

def none(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp
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

#rr = requests.get(settings.BASEURL+'/BusinessPartners/$count', cookies=r.cookies, verify=False)
res = requests.get(settings.BASEURL+'/Countries/$count', cookies=r.cookies, verify=False)
serContriesCount = int(res.text)


count = math.ceil(int(res.text)/20)
print(count)
skip=0

mycursor.execute("select * from Countries_countries")
mycursor.fetchall()
localContriesCount = mycursor.rowcount

print(f'local Contries count: {localContriesCount} and server Contries count {serContriesCount}')
if localContriesCount < serContriesCount:

    for i in range(count):
        res = requests.get(settings.BASEURL+'/Countries?$orderby=Code&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
        opts = json.loads(res.text)

        for opt in opts['value']:

            ContrieCode = opt['Code']
            ContrieName = opt['Name']
            
            selectConSql = f"select * from Countries_countries where Code='{ContrieCode}'"
            # print(selectConSql)
            mycursor.execute(selectConSql)
            mycursor.fetchall()

            if mycursor.rowcount != 1:
                contrie_ins_sql = f"INSERT INTO `Countries_countries` (`Code`, `Name`) VALUES ('{ContrieCode}', '{ContrieName}');"
                print(contrie_ins_sql)
                mycursor.execute(contrie_ins_sql)
                mydb.commit()

        print('___')
        skip = skip+20
