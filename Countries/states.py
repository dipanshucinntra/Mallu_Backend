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
res = requests.get(settings.BASEURL+'/States/$count', cookies=r.cookies, verify=False)
serStatesCount = int(res.text)


count = math.ceil(int(res.text)/20)
print(count)

mycursor.execute("select * from Countries_states")
mycursor.fetchall()
localStatesCount = mycursor.rowcount

skip=0

print(f'local State count: {localStatesCount} and server State count {serStatesCount}')
if localStatesCount < serStatesCount:

    for i in range(count):
        res = requests.get(settings.BASEURL+'/States?$orderby=Code&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
        opts = json.loads(res.text)
        # print(len(opts['value']))
        for opt in opts['value']:
            stateCode = opt['Code']
            stateCountry = opt['Country']
            stateName = opt['Name']
            selectStateSql = f"select * from Countries_states where Country='{stateCountry}' and Code='{stateCode}'"
            print(selectStateSql)
            mycursor.execute(selectStateSql)
            mycursor.fetchall()

            if mycursor.rowcount != 1:

                opp_sql = f"INSERT INTO `Countries_states` (`Code`, `Country`, `Name`) VALUES ('{stateCode}', '{stateCountry}', '{stateName}')"
                print(opp_sql)
                mycursor.execute(opp_sql)
                mydb.commit()
                #print(opp_sql)

        print('___')
        skip = skip+20


    #opts = json.loads(res.text)
    #print(len(opts['value']))

