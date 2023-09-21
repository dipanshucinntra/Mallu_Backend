import requests, json
import time

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
mycursor = mydb.cursor(dictionary=True)
#print("test comment")

# with open("../bridge/db1.json") as f:
    
r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

#res = requests.get(settings.BASEURL+'/SalesStages/', cookies=r.cookies, verify=False)
res = requests.get(settings.BASEURL+'/SalesStages?$apply=aggregate(SequenceNo with max as max_live)', cookies=r.cookies, verify=False)

#print(res.text)
live = json.loads(res.text)
#print(live['value'][0]['max_live'])
max_live = live['value'][0]['max_live']

mycursor.execute("SELECT max(`SequenceNo`) as max_local FROM `Opportunity_staticstage`")
fetch = mycursor.fetchone()
#print(fetch['max_local'])
max_local = fetch['max_local']

if str(max_local)=="None":
	print("Blank")
	res = requests.get(settings.BASEURL+'/SalesStages?$orderby=SequenceNo', cookies=r.cookies, verify=False)

	stages = json.loads(res.text)
	#print(stages)
	
	for stage in stages['value']:
		#print(stage['SequenceNo'])
		
		stage_sql = "INSERT INTO `Opportunity_staticstage` (`id`, `SequenceNo`, `Name`, `Stageno`, `ClosingPercentage`, `Cancelled`, `IsSales`, `IsPurchasing`) VALUES (NULL, '"+str(stage['SequenceNo'])+"', '"+str(stage['Name'])+"', '"+str(stage['Stageno'])+"', '"+str(stage['ClosingPercentage'])+"', '"+str(stage['Cancelled'])+"', '"+str(stage['IsSales'])+"', '"+str(stage['IsPurchasing'])+"');"
		#print(stage_sql)
		mycursor.execute(stage_sql)
		mydb.commit()
		#print('___')
		
else:	
	if(int(max_local) < max_live):
		res = requests.get(settings.BASEURL+'/SalesStages?$filter=SequenceNo gt '+max_local+' & $orderby=SequenceNo', cookies=r.cookies, verify=False)

		stages = json.loads(res.text)
		#print(stages)
		
		for stage in stages['value']:
			#print(stage['SequenceNo'])
			
			stage_sql = "INSERT INTO `Opportunity_staticstage` (`id`, `SequenceNo`, `Name`, `Stageno`, `ClosingPercentage`, `Cancelled`, `IsSales`, `IsPurchasing`) VALUES (NULL, '"+str(stage['SequenceNo'])+"', '"+str(stage['Name'])+"', '"+str(stage['Stageno'])+"', '"+str(stage['ClosingPercentage'])+"', '"+str(stage['Cancelled'])+"', '"+str(stage['IsSales'])+"', '"+str(stage['IsPurchasing'])+"');"
			#print(stage_sql)
			mycursor.execute(stage_sql)
			mydb.commit()
			#print('___')
			
