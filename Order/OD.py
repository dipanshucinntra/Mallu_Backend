import requests, json
import time
import math
import mysql.connector

from datetime import datetime

def none(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
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
print(json.loads(r.text))
if "error" in json.loads(r.text):
        print(json.loads(r.text)['error']['message']['value'])
else:
        token = json.loads(r.text)['SessionId']
        print(token)
        exit

        #rr = requests.get(settings.BASEURL+'/BusinessPartners/$count', cookies=r.cookies, verify=False)
        res = requests.get(settings.BASEURL+'/Orders/$count', cookies=r.cookies, verify=False)

        count = math.ceil(int(res.text)/20)
        print(count)

        skip=0
        for i in range(count):
            res = requests.get(settings.BASEURL+'/Orders?$orderby=DocEntry&$skip='+str(skip)+'', cookies=r.cookies, verify=False)
            opts = json.loads(res.text)
            print(len(opts['value']))

            for opt in opts['value']:
                print(opt)
                d = datetime.strptime(str(opt['DocTime']), "%H:%M:%S")
                DocTime = d.strftime("%I:%M:%S %p")

                e = datetime.strptime(str(opt['UpdateTime']), "%H:%M:%S")
                UpdateTime = e.strftime("%I:%M:%S %p")                

                discountPercent = float(opt['DiscountPercent'])
                if discountPercent < 0:
                    discountPercent = 0

                # str(discountPercent)
                ord_sql = "INSERT INTO `Order_order` (`TaxDate`, `DocDueDate`, `ContactPersonCode`, `DiscountPercent`, `DocDate`, `CardCode`, `Comments`, `SalesPersonCode`, `DocEntry`, `U_Term_Condition`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`, `CardName`, `CreationDate`, `DocCurrency`, `DocTotal`, `DocumentStatus`, `VatSum`, `BPLID`, `PaymentGroupCode`) VALUES ('"+str(opt['TaxDate'])+"', '"+str(opt['DocDueDate'])+"', '"+str(opt['ContactPersonCode'])+"', '"+str(discountPercent)+"', '"+str(opt['DocDate'])+"', '"+str(opt['CardCode'])+"', '"+str(opt['Comments'])+"', '"+str(opt['SalesPersonCode'])+"', '"+str(opt['DocEntry'])+"', '', '"+str(opt['CreationDate'])+"', '"+str(DocTime)+"', '"+str(opt['UpdateDate'])+"', '"+str(UpdateTime)+"', '"+str(opt['CardName'])+"', '"+str(opt['CreationDate'])+"', '"+str(opt['DocCurrency'])+"', '"+str(opt['DocTotal'])+"', '"+str(opt['DocumentStatus'])+"', '"+str(opt['VatSum'])+"', '', '"+str(opt['PaymentGroupCode'])+"')"
                print(ord_sql)
                mycursor.execute(ord_sql)
                mydb.commit()                
                OrderID = mycursor.lastrowid
                
                U_SCOUNTRY=""
                U_SSTATE=""
                U_SHPTYPB=""
                U_BSTATE=""
                U_BCOUNTRY=""
                U_SHPTYPS=""

                add = opt['AddressExtension']
                add_sql = "INSERT INTO `Order_addressextension` (`OrderID`, `BillToBuilding`, `ShipToState`, `BillToCity`, `ShipToCountry`, `BillToZipCode`, `ShipToStreet`, `BillToState`, `ShipToZipCode`, `BillToStreet`, `ShipToBuilding`, `ShipToCity`, `BillToCountry`, `U_SCOUNTRY`, `U_SSTATE`, `U_SHPTYPB`, `U_BSTATE`, `U_BCOUNTRY`, `U_SHPTYPS`) VALUES ('"+str(OrderID)+"', '"+str(add['BillToBuilding'])+"', '"+str(add['ShipToState'])+"', '"+str(add['BillToCity'])+"', '"+str(add['ShipToCountry'])+"', '"+str(add['BillToZipCode'])+"', '"+str(add['ShipToStreet'])+"', '"+str(add['BillToState'])+"', '"+str(add['ShipToZipCode'])+"', '"+str(add['BillToStreet'])+"', '"+str(add['ShipToBuilding'])+"', '"+str(add['ShipToCity'])+"', '"+str(add['BillToCountry'])+"', '"+str(U_SCOUNTRY)+"', '"+str(U_SSTATE)+"', '"+str(U_SHPTYPB)+"', '"+str(U_BSTATE)+"', '"+str(U_BCOUNTRY)+"', '"+str(U_SHPTYPS)+"');"
                print(add_sql)                
                mycursor.execute(add_sql)
                mydb.commit()

                for line in opt['DocumentLines']:
                    print(line['Quantity'])
                    lDiscountPercent = float(line['DiscountPercent'])
                    if lDiscountPercent < 0:
                        lDiscountPercent = 0
                    
                    str(lDiscountPercent)
                    #line_sql = "INSERT INTO `Opportunity_line` (`id`, `LineNum`, `SalesPerson`, `StartDate`, `ClosingDate`, `StageKey`, `MaxLocalTotal`, `MaxSystemTotal`, `Remarks`, `Contact`, `Status`, `ContactPerson`, `SequenceNo`, `Opp_Id`) VALUES (NULL, '"+str(line['LineNum'])+"', '"+str(line['SalesPerson'])+"', '"+str(line['StartDate'])+"', '"+str(line['ClosingDate'])+"', '"+str(line['StageKey'])+"', '"+str(line['MaxLocalTotal'])+"', '"+str(line['MaxSystemTotal'])+"', '"+str(line['Remarks'])+"', '"+str(line['Contact'])+"', '"+str(line['Status'])+"', '"+str(line['ContactPerson'])+"', '"+str(line['SequenceNo'])+"', '1');"
                    line_sql = "INSERT INTO `Order_documentlines` (`LineNum`, `OrderID`, `Quantity`, `UnitPrice`, `DiscountPercent`, `ItemCode`, `TaxCode`, `ItemDescription`, `U_FGITEM`, `CostingCode2`, `ProjectCode`, `FreeText`) VALUES ('"+str(line['LineNum'])+"', '"+str(OrderID)+"', '"+str(line['Quantity'])+"', '"+str(line['UnitPrice'])+"', '"+str(lDiscountPercent)+"', '"+str(line['ItemCode'])+"', '"+str(line['TaxCode'])+"', '"+str(line['ItemDescription'])+"', '"+str(line['U_FGITEM'])+"', '"+str(line['CostingCode2'])+"', '"+str(line['ProjectCode'])+"', '"+str(line['FreeText'])+"');"
                    print(line_sql)
                    mycursor.execute(line_sql)
                    mydb.commit()
            print('___')
            skip = skip+20

        #opts = json.loads(res.text)
        #print(len(opts['value']))

