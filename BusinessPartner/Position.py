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


ttl = requests.get(settings.BASEURL+'/EmployeePosition/$count', cookies=r.cookies, verify=False)

for t in range(int(ttl.text)):
	# url = "http://122.160.67.60:50001/b1s/v1/EmployeePosition?$top=1&$skip="+str(t)+""
 
	url = settings.BASEURL+"/EmployeePosition?$top=1&$skip="+str(t)+""
	res = requests.get(url, cookies=r.cookies, verify=False)

	bps = json.loads(res.text)
	print(len(bps['value']))
	for bp in bps['value']:
		print('-----Position---')
		print(bp['PositionID'])
		print(bp['Name'])
		print(bp['Description'])
		
		pos_sql = "INSERT INTO `BusinessPartner_bpposition` (`PositionID`, `Name`, `Description`) VALUES ('"+str(bp['PositionID'])+"', '"+str(bp['Name'])+"', '"+str(bp['Description'])+"');"

		mycursor.execute(pos_sql)
		mydb.commit()
		#print(mycursor.last_inserted_id())

