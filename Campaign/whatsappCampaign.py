from ctypes import sizeof
from datetime import date, datetime
import calendar
# from email import encoders
# from email.message import EmailMessage
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# import imghdr
# import os
# import smtplib
# import time
# import math
import mysql.connector
import requests, json

from urllib.parse import unquote
# from urllib.parse import urlparse

import sys
sys.path.append('/home/www/b2b/wiscon_tel_dev/bridge/')
from camp_fun import sendWhatsAppMsg

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="$Bridge@2022#",
# #   password="root",
#   database="wiscon_tel_dev"
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


# -------------------
# Email Campaign Body  
# -------------------
def sendCampaignToMember(Subject, Message, members, Attachments, campId):
    print('in sendCampaignToMember')
    print(Subject)
    for member in members:
        Phone = member['Phone']
        if Phone !="":
            # print('in mail functions')
            # print(Phone, Subject, Message)
            res = sendWhatsAppMsg(Phone, Message, Attachments)
            print(res)
    
            # if Frequency == 'Once':
            #     # update send status 1 in campaign
            #     sqlUpdateCampaign = "UPDATE `Campaign_campaign` SET `Sent` = 1 WHERE `id` = "+ str(campId)
            #     mycursor.execute(sqlUpdateCampaign)
            #     mydb.commit()

# def sendWhatsAppMsg(number, msg, Attachments):
#     # insetanceId = "621f17f4cd00c56ad254fd4f"
#     insetanceId = "62f0dedb0857b14e2d3775c9"
#     url = ""
#     if msg != "" and Attachments != "":
#         url = f"https://wasmsapi.com/api/sendFileWithCaption?token={insetanceId}&phone=+91{number}&message={msg}"
#         attachUrl = 'http://103.234.187.197:8042'+Attachments
#         url = url+"&link="+unquote(attachUrl)
#         loginResponse = requests.post(url, verify=False, timeout=10)
#         return json.loads(loginResponse.text)

#     elif msg == "" and Attachments != "":
#         url = f"https://wasmsapi.com/api/sendFiles?token={insetanceId}&phone=+91{number}"
#         attachUrl = 'http://103.234.187.197:8042'+Attachments
#         url = url+"&link="+unquote(attachUrl)
#         loginResponse = requests.post(url, verify=False, timeout=10)
#         return json.loads(loginResponse.text)

#     elif msg != "" and Attachments == "":
#         url = f"https://wasmsapi.com/api/sendText?token={insetanceId}&phone=+91{number}&message={msg}"
#         loginResponse = requests.post(url, verify=False, timeout=10)
#         return json.loads(loginResponse.text)
    
#     else:
#         msg = 'all field are empty! messages will not be sent'
#         print(msg)
#         return msg

userList = []

# sqlSelectCamSet = "SELECT * FROM `Campaign_campaignset` WHERE `id` = 38"
sqlSelectCamSet = "SELECT * FROM `Campaign_campaignset` WHERE Status = 1"
mycursor.execute(sqlSelectCamSet)
allRow = mycursor.fetchall()
for campaign in allRow:
    camSetId = campaign[0]
    print(camSetId)

    # -----------------------
    # campain set member list
    # -----------------------
    allMembersArr = []
    sqlSelectMember = "SELECT * FROM `Campaign_campaignsetmembers` WHERE `CampSetId_id` = "+ str(camSetId)
    mycursor.execute(sqlSelectMember)
    allMembers = mycursor.fetchall()
    if len(allMembers) != 0:
        for member in allMembers:
            userData = {
                'Name': member[1],
                'Phone': member[2],
                'Email': member[3]
            }
            allMembersArr.append(userData)


    # -----------------------
    # --- campain list ------
    # -----------------------
    mailSubject = ""
    mailbody = ""

    print('---Campaign---')
    sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `RunTime` = '"+str(currentTime)+"' AND `Status` = 1 AND `Sent` = 0 AND `Type` = 'WhatsApp' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    # sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `Status` = 1 AND `Sent` = 0 AND `Type` = 'WhatsApp' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    print(sqlSelectCam)
    mycursor.execute(sqlSelectCam)
    allCampaign = mycursor.fetchall()
    print(len(allCampaign))
    if len(allCampaign) != 0:
        for campaign in allCampaign:
            # print(campaign)
            camp_id = campaign[0]
            
            Frequency = campaign[5]
            WeekDay = campaign[6]
            MonthlyDate = campaign[7]
            mailbody = campaign[8]
            mailSubject = campaign[17]
            RunTime = campaign[21]
            Attachments = campaign[20]

            if Frequency == 'Daily':
                # if RunTime == currentTime:
                sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Weekly':
                days = WeekDay.split(",")
                if currentDay in days:
                    sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Monthly':
                dates = MonthlyDate.split(",")
                if currentDate in dates:
                    sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

            elif Frequency == 'Once':
                sendCampaignToMember(mailSubject, mailbody, allMembersArr, Attachments, camp_id)

