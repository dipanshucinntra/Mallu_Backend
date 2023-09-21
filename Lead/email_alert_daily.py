# ###################################################################
# ###################################################################
# ######## Run every day-of-week from Monday through Friday #########
# ###################################################################
# ###################################################################

# “At 09:30 on every day-of-week from Monday through Friday.”
# 30 9 * * 1-5 /usr/bin/python3 /home/www/b2b/wiscon_tel_dev/bridge/Lead/email_alert_daily.py

tempFile = open('tempDaily.txt', 'w')
tempFile.write('Create a new text file!')

from datetime import date, datetime
import calendar
import mysql.connector

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

# if currentDay != 'Saturday' or currentDay != 'Sunday':
#     # print('day ok')
#     if currentTime == "09:30 AM":
#         # print('time ok ')

import sys
sys.path.append('/home/www/b2b/wiscon_tel_dev/bridge/')
# sys.path.append('../../wiscon_tel_dev')
from camp_fun import sendMail

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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>> List Employee >>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
sqlSelectEmployee = "SELECT `id`,`SalesEmployeeCode`,`SalesEmployeeName`,`Email`,`Mobile` FROM `Employee_employee` WHERE `role` != 'admin' ORDER BY `id` ASC"
mycursor.execute(sqlSelectEmployee)
allEmp = mycursor.fetchall()
if len(allEmp)!= 0:
    for emp in allEmp:
        print('---Employee---')
        id = emp[0]
        SalesEmployeeCode = emp[1]
        SalesEmployeeName = emp[2]
        Email = emp[3]
        Mobile = emp[4]
        print(Email)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>> List Lead by Employee >>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlSelectLead = "SELECT id, companyName, contactPerson, phoneNumber, source, groupType, intProdCat, intProjCat, location, leadType  FROM `Lead_lead` WHERE `status` = 'Not Qualified' AND `leadType`= 'New' AND `assignedTo_id` = "+str(id)
        print(sqlSelectLead)
        mycursor.execute(sqlSelectLead)
        allLead = mycursor.fetchall()
        if len(allLead) != 0:
            leadRow = ""

            for lead in allLead:
                print('---lead---')
                
                leadRow += f""" 
                    <tr>
                        <td>{lead[0]}</td>
                        <td>{lead[1]}</td>
                        <td>{lead[2]}</td>
                        <td>{lead[3]}</td>
                        <td>{lead[4]}</td>
                        <td>{lead[5]}</td>
                        <td>{lead[6]}</td>
                        <td>{lead[7]}</td>
                        <td>{lead[8]}</td>
                        <td>{lead[9]}</td>
                    </tr>
                """
        
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # after creating lead mail alert to reporting person
            empFirstName = SalesEmployeeName
            empEmail = Email
            mailSubject = "List of Leads for FollowUp, and List of New Leads"
            mailMessage = f"""
            <div>
                Hi Sir/Mam <b>{empFirstName}</b>,<br><br>
                You'r assigned lead are: <br><br>
            </div>
            <table style="width: 100%">
            <tr>
                <th>Lead Id</th>
                <th>Company Name</th>
                <th>Contact Person</th>
                <th>Phone Number</th>
                <th>Source</th>
                <th>Group Type</th>
                <th>Interested in Product Category </th>
                <th>Interested in Project Category </th>
                <th>Zone Stage</th>
                <th>Stage</th>
            </tr>
            {leadRow}
            </table>"""
            mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = "")
            print(mailResponse)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>