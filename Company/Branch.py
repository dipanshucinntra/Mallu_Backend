import json
import pyodbc

server = '122.160.67.60' # to specify an alternate port
#server = 'tcp:myserver.database.windows.net' 
database = 'BRIDGE' 
username = 'sa' 
password = 'Sa@2017'

url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
print(url)
conn = pyodbc.connect(url)
cursor = conn.cursor()

#cursor.execute("SELECT @@version;")
#cursor.execute("SELECT * from OBPL")
cursor.execute("SELECT BPLId, BPLName, Address, MainBPL, Disabled, UserSign2, UpdateDate, DflWhs, TaxIdNum, StreetNo, Building, ZipCode, City, State, Country from OBPL where Disabled='N'") 
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]
all = []
i=0;


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="$Bridge@2022#",
  database="wiscon_pre"
)



mycursor = mydb.cursor()



for row in rows:
  sp_sql = "INSERT INTO `Company_branch` (`BPLId`, `BPLName`, `Address`, `MainBPL`, `Disabled`, `UserSign2`, `UpdateDate`, `DflWhs`, `TaxIdNum`, `StreetNo`, `Building`, `ZipCode`, `City`, `State`, `Country`) VALUES ('"+str(row[0])+"', '"+str(row[1])+"', '"+str(row[2])+"', '"+str(row[3])+"', '"+str(row[4])+"', '"+str(row[5])+"', '"+str(row[6])+"', '"+str(row[7])+"', '"+str(row[8])+"', '"+str(row[9])+"', '"+str(row[10])+"', '"+str(row[11])+"', '"+str(row[12])+"', '"+str(row[13])+"', '"+str(row[14])+"');"
  print(sp_sql)
  mycursor.execute(sp_sql)
  mydb.commit()

