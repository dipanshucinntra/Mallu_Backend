import requests, json
import time
import math
import mysql.connector

def none(inp):
        if inp.lower()=="none":
            return "x";
        else:
            return inp

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sunil@123",
  database="vision_test"
)
mycursor = mydb.cursor()
print("test comment")



    
    




r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

res = requests.get(settings.BASEURL+'/BusinessPartners', cookies=r.cookies, verify=False)

bps = json.loads(res.text)
print(len(bps['value']))
for bp in bps['value']:
    print('-----Business Partner---')
    bpcode = bp['CardCode']
    print(bp['CardCode'])
    print(bp['CardName'])
    print(bp['Industry'])
    print(bp['CardType'])
    print(bp['Website'])
    print(bp['EmailAddress'])
    print(bp['Phone1'])
    print(bp['DiscountPercent'])
    print(bp['Currency'])
    print(bp['IntrestRatePercent'])
    print(bp['CommissionPercent'])
    print(bp['AttachmentEntry'])
    print(bp['CreateDate'])
    print(bp['CreateTime'])
    print(bp['UpdateDate'])
    print(bp['UpdateTime'])

    opp_sql = "INSERT INTO `BusinessPartner_businesspartner` (`BPAddresses`, `CardCode`, `SalesPersonCode`, `ContactPerson`, `CardName`, `Notes`, `PayTermsGrpCode`, `CreditLimit`, `Industry`, `CardType`, `Website`, `EmailAddress`, `Phone1`, `DiscountPercent`, `Currency`, `IntrestRatePercent`, `CommissionPercent`, `AttachmentEntry`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(bp['BPAddresses'])+"', '"+str(bp['CardCode'])+"', '"+str(bp['SalesPersonCode'])+"', '"+str(bp['ContactPerson'])+"', '"+str(bp['CardName'])+"', '"+str(bp['Notes'])+"', '"+str(bp['PayTermsGrpCode'])+"', '"+str(bp['CreditLimit'])+"', '"+str(bp['Industry'])+"', '"+str(bp['CardType'])+"', '"+str(bp['Website'])+"', '"+str(bp['EmailAddress'])+"', '"+str(bp['Phone1'])+"', '"+str(bp['DiscountPercent'])+"', '"+str(bp['Currency'])+"', '"+str(bp['IntrestRatePercent'])+"', '"+str(bp['CommissionPercent'])+"', '"+str(bp['AttachmentEntry'])+"', '"+str(bp['CreateDate'])+"', '"+str(bp['CreateTime'])+"', '"+str(bp['UpdateDate'])+"', '"+str(bp['UpdateTime'])+"');"
    mycursor.execute(opp_sql)
    mydb.commit()
    #print(mycursor.last_inserted_id())
    bpid = mycursor.lastrowid
    print("Company ID: "+str(bpid))

    print('-----BPAddresses---')
    if len(bp['BPAddresses']) > 0:
        print(len(bp['BPAddresses']))
        for branch in bp['BPAddresses']:
            print(branch['BPCode'])
            print(branch['AddressName'])
            print(branch['AddressName2'])
            print(branch['AddressName3'])
            print(branch['BuildingFloorRoom'])
            print(none(branch['Street']))
            print(none(branch['Block']))
            print(branch['County'])
            print(branch['City'])
            print(branch['State'])
            print(branch['ZipCode'])
            print(branch['Country'])
            print(branch['AddressType'])
            print(branch['TaxOffice'])
            print(branch['GSTIN'])
            print(branch['GstType'])
            print(branch['CreateDate'])
            print(branch['CreateTime'])

            branch_sql = "INSERT INTO `Businesspartner_bpbranch` (`CompanyId`, `BPCode`, `AddressName`, `AddressName2`, `AddressName3`, `BuildingFloorRoom`, `Street`, `Block`, `County`, `City`, `State`, `ZipCode`, `Country`, `AddressType`, `TaxOffice`, `GSTIN`, `GstType`, `CreateDate`, `CreateTime`) VALUES ('"+str(bpid)+"', '"+str(branch['BPCode'])+"', '"+str(branch['AddressName'])+"', '"+str(branch['AddressName2'])+"', '"+str(branch['AddressName3'])+"', '"+str(branch['BuildingFloorRoom'])+"', '"+str(none(branch['Street']))+"', '"+str(none(branch['Block']))+"', '"+str(branch['County'])+"', '"+str(branch['City'])+"', '"+str(branch['State'])+"', '"+str(branch['ZipCode'])+"', '"+str(branch['Country'])+"', '"+str(branch['AddressType'])+"', '"+str(branch['TaxOffice'])+"', '"+str(branch['GSTIN'])+"', '"+str(branch['GstType'])+"', '"+str(branch['CreateDate'])+"', '"+str(branch['CreateTime'])+"');"
            mycursor.execute(branch_sql)
            mydb.commit()


    print('-----ContactEmployees---')

    if len(bp['ContactEmployees']) > 0:
        print(len(bp['ContactEmployees']))
        for emp in bp['ContactEmployees']:
            print("Company ID: "+str(bpid))
            print(emp['Title'])
            print(emp['FirstName'])
            print(emp['MiddleName'])
            print(emp['LastName'])
            print(emp['Position'])
            print(emp['Address'])
            print(emp['MobilePhone'])
            print(emp['Fax'])
            print(emp['E_Mail'])
            print(emp['Remarks1'])
            print(emp['InternalCode'])
            print(emp['DateOfBirth'])
            print(emp['Gender'])
            print(emp['Profession'])
            print(emp['CreateDate'])
            print(emp['CreateTime'])
            print(emp['UpdateDate'])
            print(emp['UpdateTime'])

            emp_sql = "INSERT INTO `Businesspartner_bpemployee` (`CompanyId`, `BPCode`, `Title`, `FirstName`, `MiddleName`, `LastName`, `Position`, `Address`, `MobilePhone`, `Fax`, `E_Mail`, `Remarks1`, `InternalCode`, `DateOfBirth`, `Gender`, `Profession`, `CreateDate`, `CreateTime`, `UpdateDate`, `UpdateTime`) VALUES ('"+str(bpid)+"', '"+str(bpcode)+"', '"+str(emp['Title'])+"', '"+str(emp['FirstName'])+"', '"+str(emp['MiddleName'])+"', '"+str(emp['LastName'])+"', '"+str(emp['Position'])+"', '"+str(emp['Address'])+"', '"+str(emp['MobilePhone'])+"', '"+str(emp['Fax'])+"', '"+str(emp['E_Mail'])+"', '"+str(emp['Remarks1'])+"', '"+str(emp['InternalCode'])+"', '"+str(emp['DateOfBirth'])+"', '"+str(emp['Gender'])+"', '"+str(emp['Profession'])+"', '"+str(emp['CreateDate'])+"', '"+str(emp['CreateTime'])+"', '"+str(emp['UpdateDate'])+"', '"+str(emp['UpdateTime'])+"');"
            mycursor.execute(emp_sql)
            mydb.commit()
