import json
import pyodbc

server = '122.160.67.60' # to specify an alternate port
#server = 'tcp:myserver.database.windows.net' 
database = 'TEST1003' 
username = 'sa' 
password = 'vision@1091'

url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
print(url)
conn = pyodbc.connect(url)
cursor = conn.cursor()

#cursor.execute("SELECT @@version;")
#cursor.execute("SELECT * from OBPL")
cursor.execute("SELECT CurrCode,CurrName,DocCurrCod from OCRN") 
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]
all = []
i=0;
print(columns)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="vision_test"
)
mycursor = mydb.cursor()



for row in rows:
  #print(row)
  sp_sql = "INSERT INTO `businesspartner_bpcurrency` (`CurrCode`, `CurrName`, `DocCurrCod`) VALUES ('"+str(row[0])+"', '"+str(row[1])+"', '"+str(row[2])+"');"
  print(sp_sql)
  mycursor.execute(sp_sql)
  mydb.commit()

