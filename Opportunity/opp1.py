import requests, json
import time
import math
import mysql.connector
from functions import mylib

def none(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Sunil@123",
#   database="vision_test"
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

#rr = requests.get(settings.BASEURL+'/BusinessPartners/$count', cookies=r.cookies, verify=False)
res = requests.get(settings.BASEURL+'/SalesOpportunities/$count', cookies=r.cookies, verify=False)

count = math.ceil(int(res.text)/20)
print(count)

skip=0
for i in range(count):
    res = requests.get(settings.BASEURL+'/SalesOpportunities?$orderby=SequentialNo&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
    opts = json.loads(res.text)
    print(len(opts['value']))

    for opt in opts['value']:
        #print(opt['SequentialNo'])
        opp_sql = "INSERT INTO `Opportunity_opportunity` (`id`, `SequentialNo`, `CardCode`, `SalesPerson`, `SalesPersonName`, `ContactPerson`,  `ContactPersonName`, `Source`, `StartDate`, `PredictedClosingDate`, `MaxLocalTotal`, `MaxSystemTotal`, `Remarks`, `Status`, `ReasonForClosing`, `TotalAmountLocal`, `TotalAmounSystem`, `CurrentStageNo`, `CurrentStageNumber`, `CurrentStageName`, `OpportunityName`, `Industry`, `LinkedDocumentType`, `DataOwnershipfield`, `DataOwnershipName`, `StatusRemarks`, `ProjectCode`, `CustomerName`, `ClosingDate`, `ClosingType`, `OpportunityType`, `UpdateDate`, `UpdateTime`, `U_TYPE`, `U_LSOURCE`,`U_FAV`,`U_PROBLTY`) VALUES (NULL, '"+str(opt['SequentialNo'])+"', '"+str(opt['CardCode'])+"', '"+str(opt['SalesPerson'])+"', '', '"+str(opt['ContactPerson'])+"', '', '"+str(opt['Source'])+"', '"+str(opt['StartDate'])+"', '"+str(opt['PredictedClosingDate'])+"', '"+str(opt['MaxLocalTotal'])+"', '"+str(opt['MaxSystemTotal'])+"', '"+str(opt['Remarks'])+"', '"+str(opt['Status'])+"', '"+str(opt['ReasonForClosing'])+"', '"+str(opt['TotalAmountLocal'])+"', '"+str(opt['TotalAmounSystem'])+"', '"+str(opt['CurrentStageNo'])+"', '"+str(opt['CurrentStageNumber'])+"', '', '"+str(opt['OpportunityName'])+"', '"+str(opt['Industry'])+"', '"+str(opt['LinkedDocumentType'])+"',  '"+str(none(opt['DataOwnershipfield']))+"', '', '"+str(opt['StatusRemarks'])+"', '"+str(opt['ProjectCode'])+"', '"+str(opt['CustomerName'])+"', '"+str(opt['ClosingDate'])+"', '"+str(opt['ClosingType'])+"', '"+str(opt['OpportunityType'])+"', '"+str(opt['UpdateDate'])+"', '"+str(opt['UpdateTime'])+"', '','','','');"
        mycursor.execute(opp_sql)
        mydb.commit()

        #print(len(opt['SalesOpportunitiesLines']))
        for line in opt['SalesOpportunitiesLines']:
            #print(line['LineNum'])
            line_sql = "INSERT INTO `Opportunity_line` (`id`, `LineNum`, `SalesPerson`, `StartDate`, `ClosingDate`, `StageKey`, `MaxLocalTotal`, `MaxSystemTotal`, `Remarks`, `Contact`, `Status`, `ContactPerson`, `SequenceNo`, `Opp_Id`) VALUES (NULL, '"+str(line['LineNum'])+"', '"+str(line['SalesPerson'])+"', '"+str(line['StartDate'])+"', '"+str(line['ClosingDate'])+"', '"+str(line['StageKey'])+"', '"+str(line['MaxLocalTotal'])+"', '"+str(line['MaxSystemTotal'])+"', '"+str(line['Remarks'])+"', '"+str(line['Contact'])+"', '"+str(line['Status'])+"', '"+str(line['ContactPerson'])+"', '"+str(line['SequenceNo'])+"', '1');"
            mycursor.execute(line_sql)
            mydb.commit()
    print('___')
    skip = skip+20


#opts = json.loads(res.text)
#print(len(opts['value']))

