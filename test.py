from cmath import e
import csv
from datetime import datetime
from itertools import count
import smtplib
from email.message import EmailMessage
from tkinter import E
from Database.database import Database as db
from smtplib import *
import time



# studentsLogins =[]
# #csv keeping student data
# with open('student_data.csv', 'r') as stFile:
#     row = csv.reader(stFile)
#     for item in row:
#         studentsLogins.append(item)
  

            
# def authenticate(stid, indexNo):
#     for i in range(len(studentsLogins)):
#         for k in range(len(studentsLogins)):
#             if(studentsLogins[i][k]==stid and studentsLogins[i][k+1] == indexNo):
#                 return studentsLogins[i][k+2]
#     return False

# print(authenticate("20592316",'4620618'))
#authentication routine      
# def match(stId, stIndex):
#     for row in studentsLogins:
#         list = []
#         list.append(row[0])
#         list.append(row[1])
#         print(list)
#         if(list[0] == stId and stIndex == ' 20592316'):
#             print(list[0])
#             print(list[1])
#             print('pass')     
#             return True

# print(match('Saeed Bashr', ' 20592316'))


# def sendMail(subject, body, to):
    
#     SENDER = 'aamustedcounsellingcentre22@gmail.com'
#     PASSWORD = "ucncdfzqavwzayxb" #aamusted@22 
    
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['subject'] = subject
#     msg['to'] = to
#     msg['from'] = SENDER
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER, PASSWORD)
#         server.send_message(msg)  
#         print("success")    
#         server.quit()
#     except Exception as e:
#         # error_code = e.smtp_code
#         print("Error snding message ")
        
# sendMail("Python fundamentals", "this message is from python","sumailaadams438@gmail.com")

# times = db.executeQuery('SELECT start_time, end_time FROM Available_Counsellor WHERE start_time = "12:00" AND end_time = "17:00"')

# print(times)

# data = db.executeQuery("SELECT * FROM Available_Counsellor WHERE Name='Prof Mohammed Hafiz'")
# print(data[0][7])
# btime = int(data[0][5].replace(":","")[:4])
# print(data[0][5])
# print(time.ctime())
# name = "PROF MOHAMMED HAFIZ"
# counsellortime = db.executeQuery(f"SELECT * FROM Available_Counsellor WHERE Name='ADMIN ADMIN'") 
# print(type(counsellortime[0][3]))

# curr = time.ctime().split(" ")[:4]
# print(curr)
# Name = "Adams"
# n = db.countBookings(f"SELECT COUNT(Name) FROM Student_Apppointment_Record WHERE Name = '{Name}'")

now = datetime.utcnow()



dt_str = '27/10/20 05:23:20'

dt_obj = datetime.strptime(dt_str, '%d/%m/%y %H:%M:%S')


def remove_from_available_lecturers(timenow):
    get_available_lec = db.executeQuery(f"SELECT Name FROM Available_Counsellor WHERE end_time <'{timenow}'")
    return (get_available_lec)
 

# lec = remove_from_available_lecturers(datetime.utcnow())

# timenow = str(time.gmtime().tm_mday)+"/"+str(time.gmtime().tm_mon)+"/"+str(time.gmtime().tm_year)[2:]+" "+str(time.gmtime().tm_hour)+":"+str(time.gmtime().tm_min)+":"+str(time.gmtime().tm_sec)
dt = str(time.gmtime().tm_hour)+":"+str(time.gmtime().tm_min)

# get_available_lec = db.executeQuery("SELECT Name FROM Available_Counsellor WHERE end_time ='19:08'")
t = str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
lec = remove_from_available_lecturers("08:30")
db.executeQuery(f"DELETE Name FROM Available_Counsellor WHERE end_time = '{lec}'")
print(lec)
