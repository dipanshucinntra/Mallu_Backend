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

ttl = requests.get(settings.BASEURL+'/SalesPersons/$count', cookies=r.cookies, verify=False)

for t in range(int(ttl.text)):
	# url = "http://122.160.67.60:50001/b1s/v1/SalesPersons?$top=1&$skip="+str(t)+""
	url = settings.BASEURL+"/SalesPersons?$top=1&$skip="+str(t)+""

	res = requests.get(url, cookies=r.cookies, verify=False)

	sps = json.loads(res.text)
	print(len(sps['value']))
	for sp in sps['value']:
		print('-----SalePersons---')
		print(sp['SalesEmployeeCode'])
		print(sp['SalesEmployeeName'])
		print(sp['Remarks'])
		print(sp['CommissionForSalesEmployee'])
		print(sp['CommissionGroup'])
		print(sp['Locked'])
		print(sp['EmployeeID'])
		if sp['EmployeeID'] == None:
			EmployeeID = ""
		print(sp['Active'])
		print(sp['Telephone'])
		print(sp['Mobile'])
		print(sp['Fax'])
		print(sp['Email'])

		sp_sql = "INSERT INTO `Employee_employee` (`companyID`, `userName`, `password`, `firstName`, `middleName`, `lastName`, `role`, `position`, `branch`, `passwordUpdatedOn`, `lastLoginOn`, `logedIn`, `reportingTo`, `timestamp`, `SalesEmployeeCode`, `SalesEmployeeName`, `EmployeeID`, `Active`, `Mobile`, `Email`, `FCM`) VALUES ('', '', '', '"+str(sp['SalesEmployeeName'])+"', '', '', '', '', '', '', '', '', '', '', '"+str(sp['SalesEmployeeCode'])+"', '"+str(sp['SalesEmployeeName'])+"', '"+EmployeeID+"', '"+str(sp['Active'])+"', '"+str(sp['Mobile'])+"', '"+str(sp['Email'])+"', '');"
		print(sp_sql)

		mycursor.execute(sp_sql)
		mydb.commit()
		spid = mycursor.lastrowid
		print(spid)

