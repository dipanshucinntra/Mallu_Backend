import requests, json
import time
import math
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sunil@123",
  database="cinntra_app"
)
mycursor = mydb.cursor()
print("test comment")

#data = {"CompanyDB":"INTERNAL_APP","Password":"Abcd@123","UserName":"manager"}
data = {"CompanyDB":"TEST","Password":"Qwer1234","UserName":"manager"}

r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

opp_data = {
  "CardCode": "C00002",
  "PredictedClosingDate": "2021-9-17",
  "ContactPerson": "7",
  "MaxLocalTotal": 500000.0,
  "MaxSystemTotal": 0.0,
  "Remarks": "Testing Bp 2 sept.",
  "SalesOpportunitiesLines": [
    {
      "DocumentType": "bodt_MinusOne",
      "MaxLocalTotal": 500000.0,
      "MaxSystemTotal": 0.0,
      "SalesPerson": 5,
      "StageKey": "2"
    }
  ],
  "SalesPerson": 5,
  "StartDate": "2021-09-03",
  "U_FAV": "No",
  "U_LSOURCE": "Webinar",
  "U_PROBLTY": "0.5",
  "U_TYPE": "New Business",
  "OpportunityName": "Test post by sk"
}

#rr = requests.get(settings.BASEURL+'/BusinessPartners/$count', cookies=r.cookies, verify=False)
res = requests.post(settings.BASEURL+'/SalesOpportunities', data=json.dumps(opp_data), cookies=r.cookies, verify=False)
print(res.text)
live = json.loads(res.text)
print(live['SequentialNo'])
