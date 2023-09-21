import requests, json
import time
import math
import mysql.connector
import pandas as pd
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="$Bridge@2022#",
  database="vision_dev"
)
mycursor = mydb.cursor(dictionary=True)
#print("test comment")


############# start data from local sql#########
try:
    #SQL_Query = pd.read_sql_query('select ItemCode, InStock from Item_item', mydb)
    SQL_Query = pd.read_sql_query('SELECT * FROM `Item_item` order by ItemCode', mydb)    
    local_item = pd.DataFrame(SQL_Query, columns=['ItemCode', 'InStock'])
    #local_item.drop(local_item.loc[local_item['ItemCode']=='002052040M'].index, inplace=True) #working
    #local_item = local_item[local_item['ItemCode'] != '002052040M'] # working
    #local_item.set_index("ItemCode", inplace = True)
    #print(local_item)
except:
    print("Error: unable to convert the data")


############# end data from local sql#########

with open("/home/www/b2b/vision_dev/bridge/bridge/db.json") as f:
    
    




r = requests.post(settings.BASEURL+'/Login', data=json.dumps(settings.SAPDB), verify=False)
token = json.loads(r.text)['SessionId']
print(token)

count = requests.get("http://122.160.67.60:50001/b1s/v1/Items/$count", cookies=r.cookies, verify=False).text
print(count)

############# start data from server sap #########
res = requests.get("http://122.160.67.60:50001/b1s/v1/Items?$orderby=ItemCode&$select=ItemCode,QuantityOnStock", cookies=r.cookies, headers={"Prefer":"odata.maxpagesize="+str(count)+""}, verify=False)
#res = requests.get("http://122.160.67.60:50001/b1s/v1/DistributionRules?$select=FactorCode,FactorDescription&$filter=InWhichDimension eq 2", cookies=r.cookies, verify=False)
whs = json.loads(res.text)
#print(len(whs['value']))

server_item = pd.DataFrame(whs['value'], columns=['ItemCode', 'QuantityOnStock'])
#server_item.set_index("ItemCode", inplace = True)
#print(server_item)
############# end data from server sap #########


#print("check missing_values")
missing_values = set(local_item.iloc[:, 0]).symmetric_difference(set(server_item.iloc[:, 0]))
print(missing_values)

for miss in missing_values:
    #print(miss)
    local_item.drop(local_item.loc[local_item['ItemCode']==miss].index, inplace=True)
    server_item.drop(server_item.loc[server_item['ItemCode']==miss].index, inplace=True)

local_item = local_item.reset_index(drop=True)
server_item = server_item.reset_index(drop=True)

#local_item.sort_values(by=['ItemCode'], ascending=True)
#server_item.sort_values(by=['ItemCode'], ascending=True)

print('------clean-----')
print(len(local_item))
print(len(server_item))

#print(local_item)
#print(server_item)

#local_item.drop(local_item.loc[local_item['ItemCode']=='002052040M'].index, inplace=True) #working

############# start data cpmpare #########

#local_item['QuantityOnStock'] = server_item['QuantityOnStock']
#local_item['stock_match'] = np.where(local_item['InStock'] == server_item['QuantityOnStock'], "True", "False")
#local_item.sort_index(inplace=False)

try:
    server_item_diff = server_item.loc[local_item['InStock'] != server_item['QuantityOnStock']]
    print(len(server_item_diff))

    if len(server_item_diff) !=0:
        print(server_item_diff)
        #quit()
        for it in server_item_diff['ItemCode']:
            print(it)
            itm = server_item.loc[it == server_item['ItemCode']]
            stk = itm['QuantityOnStock'].to_string(index=False)
            sql ="update Item_item SET InStock='"+str(stk).strip()+"' where ItemCode='"+str(it)+"'"
            print(sql)
            #mycursor.execute(sql)
            #mydb.commit()
            #print(itm['QuantityOnStock'])

except Exception as e:
    print(e)


mydb.close()

"""
############# end data cpmpare #########


res = requests.get(settings.BASEURL+'/Items/$count', cookies=r.cookies, verify=False)
#print(res.text)

pages = math.ceil(int(res.text)/20)
#print(pages)

skip=0

for page in range(pages):
        res = requests.get("http://122.160.67.60:50001/b1s/v1/Items?$select=ItemCode,ItemName,U_DIV,ItemsGroupCode&$skip="+str(skip), cookies=r.cookies, verify=False)

        items = json.loads(res.text)

        for item in items['value']:
            print('-----Item---')
            print(item['ItemName'])
            ItemName = item['ItemName'].replace("'", "''")
            print(item['ItemCode'])
            #print(item['ItemPrices'][0]['Price'])
            #price = str(none(item['ItemPrices'][0]['Price']))
            price = str(0)
            
            print("select ItemCode from Item_item where ItemCode='"+str(item['ItemCode'])+"'")
            mycursor.execute("select * from Item_item where ItemCode='"+str(item['ItemCode'])+"'")
            mycursor.fetchall()
            rc = mycursor.rowcount
            print(rc)
            if rc != 1:
                item_sql = "INSERT INTO `Item_item` (`UnitPrice`, `Currency`, `DiscountPercent`, `ItemCode`, `TaxCode`, `ItemName`, `U_DIV`, `ItemsGroupCode_id`) VALUES ('"+price+"', 'INR', '0', '"+str(item['ItemCode'])+"', 'IGST12', '"+str(ItemName)+"', '"+str(item['U_DIV'])+"', '"+str(item['ItemsGroupCode'])+"');"
                print(item_sql)
                mycursor.execute(item_sql)
                mydb.commit()
            #itemid = mycursor.lastrowid
            #print(itemid)

        print('___')
        skip = skip+20
"""
