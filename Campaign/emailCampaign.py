from ctypes import sizeof
from datetime import date, datetime
import calendar
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import imghdr
import os
import smtplib
import requests, json
import time
import math
import mysql.connector

from urllib.parse import urlparse

import sys
sys.path.append('/home/www/b2b/wiscon_tel_dev/bridge/')
# sys.path.append('../../wiscon_tel_dev')
from camp_fun import sendMail

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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -------------------
# Email Campaign Body
# -------------------
def sendCampaignToMember(Subject, Message, members, Attachments, campId):
    print('in sendCampaignToMember')
    print(Subject)
    for member in members:
        email = member['Email']
        if email !="":
            # print('in mail functions')
            # print(email, Subject, Message)
            res = sendMail(toEmail= email, subject = Subject, message = Message, attachments = Attachments)
            print(res)
    
            if Frequency == 'Once':
                # update send status 1 in campaign
                sqlUpdateCampaign = "UPDATE `Campaign_campaign` SET `Sent` = 1 WHERE `id` = "+ str(campId)
                mycursor.execute(sqlUpdateCampaign)
                mydb.commit()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

userList = []
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
    sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `RunTime` = '"+str(currentTime)+"' AND `Status` = 1 AND `Sent` = 0 AND `Type` = 'Email' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
    # sqlSelectCam = "SELECT * FROM `Campaign_campaign` WHERE `Status` = 1 AND `Sent` = 0 AND `Type` = 'Email' AND `StartDate` <= '"+str(currentDate)+"' AND `EndDate` >= '"+str(currentDate)+"' AND `CampaignSetId_id` = "+ str(camSetId)
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
            Attachments = campaign[19]

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

