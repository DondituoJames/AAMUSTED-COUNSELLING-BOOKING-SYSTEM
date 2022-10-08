from asyncore import read
from compileall import compile_dir
from concurrent.futures.process import _python_exit
from flask import Flask, render_template, session, url_for,redirect, request
from Database.database import Database as db
import random
import time
from email.message import EmailMessage
import smtplib
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'I will never regret you nor wish to never met you because once upon a time you were exactly what i wanted'



def remove_from_available_lecturers(timenow):
    get_available_lec = db.executeQuery(f"DELETE Name FROM Available_Counsellor WHERE end_time <= '{timenow}'")
    return list(get_available_lec) 
    
def sendMail(subject, body,to):
    SENDER = 'aamustedcounsellingcentre22@gmail.com'
    PASSWORD = "ucncdfzqavwzayxb" #aamusted@22 
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = SENDER
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()
       
def getList(result, ls, uniq):
    for i in result:
        ls.append(i[0].upper())
   
    for item in ls:
        if item not in uniq:
            uniq.append(item)
    return uniq
    
    


    
# studentsLogins = []


#csv keeping student data
# with open('student_data.csv', 'r') as stFile:
#     row = csv.reader(stFile)
#     print(row)
#     for item in row:
#         studentsLogins.append(item)
  
#authentication routine      
# def authenticate(stid, indexNo):
#     for i in range(len(studentsLogins)):
#         for k in range(len(studentsLogins)):
#             if(studentsLogins[i][k]==stid and studentsLogins[i][k+1] == indexNo):
#                 return studentsLogins[i][k+2]
#     return False
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/appointment", methods=["GET"])
def newAppointment():
    ls=[]
    uniq =[]
    counsellors = db.executeQuery("SELECT name FROM Available_Counsellor")
    counsellorName = getList(counsellors, ls, uniq)
    
    booking_time = time.gmtime()
        
    lec_time_over = db.executeQuery(f"SELECT Name FROM Available_Counsellor WHERE end_time > '{str(booking_time.tm_hour +12)}'")

    to_remove_sechedule = []
    for t in lec_time_over:
        to_remove_sechedule.append(t[0])
            
        # remove lectures with expired schedule from the database
    for i in to_remove_sechedule:
        db.executeQuery(f"DELETE FROM Available_Counsellor WHERE end_time  > '{i}'")
    
    return render_template('appointment-new.html', len = len(counsellorName), counsellorName=counsellorName)

# @app.route("/new-appointment", methods=["POST","GET"])
# def new():
#     if request.method == "POST":
#         sid = request.form['stid']
#         index = request.form['stpassword']
#         print(sid, index)
#         success = authenticate(sid, index)
#         if success != False:
#             sname = success
#             return render_template('student_form.html',sname=sname)
#         else:
#             return '<p>wrong combination of credentials</p>'
        
#     return redirect(url_for('home'))

@app.route("/student-appointment", methods=["POST", "GET"])
def new():
    if request.method == "GET":
        redirect(url_for('home'))
    else:
        sid = request.form['stid']
        index = request.form['stpassword']
        return_data = db.get_student((sid, index))
        
        if len(return_data) != 0: 
            ls=[]
            uniq =[]
            counsellors = db.executeQuery("SELECT name FROM Available_Counsellor")
            counsellorName = getList(counsellors, ls, uniq)
            return_data = return_data[0]
            sname = return_data[0]
            ssname = return_data[3]
            faculty = return_data[4]
            sdepartment = return_data[5]
            print(sdepartment)
            phone_number = return_data[6]
            semail = return_data[7]
            session['name'] = return_data[0]
            session['stid'] = return_data[1]
            session['stpassword'] = return_data[2]
            
            
            return render_template('student_form.html', sname=sname, len=len(counsellorName), counsellorName=counsellorName, ssname=ssname,phone_number=phone_number, semail=semail, faculty=faculty,sdepartment=sdepartment)
        else:
            return render_template("student-login-error.html")
        
@app.route("/lecturer-appointment", methods=["POST", "GET"])
def newLectAppointment():
    if request.method == "GET":
        return redirect(url_for('home'))
    else:
        lecid = request.form['staffId'] #this is just the email
        lecpass = request.form['staffpassword'] #this is the ID
        Lecturer = db.executeQuery(f"SELECT * FROM lecturer_Profiles WHERE Name='{lecid}'")
        department = Lecturer[0][7]
        faculty = Lecturer[0][6]
        phone = Lecturer[0][5]
        
        return_data = db.get_lec((lecid, lecpass))
        if len(return_data) != 0:
            ls=[]
            uniq =[]
            counsellors = db.executeQuery("SELECT name FROM Available_Counsellor")
            counsellorName = getList(counsellors, ls, uniq)
            return_data = return_data[0]
            session['name'] = return_data[0]
            session['staffId'] = return_data[1]
            session['staffpassword'] = return_data[2]
            session['fname'] = return_data[3]
            session['sname'] = return_data[4]
            
            fname = return_data[3]
            sname = return_data[4]
            return render_template('lecturer_form.html', lecid=lecid, fname=fname, sname=sname, len=len(counsellorName),counsellorName=counsellorName, phone=phone, faculty=faculty, department=department)
        else:
            return render_template("lecturer-login-error.html")

@app.route("/non-reg-complete-app", methods=["POST", "GET"])
def completeAppointment():
    if request.method == "GET":
        return redirect(url_for('home'))
    else:
        name = request.form['oname']
        phone = request.form['ophone']
        oid = request.form['oid']
        dob = request.form['odob']
        marriage = request.form['Omarriage']
        work_type = request.form['Owork_type']
        emp_sector = request.form['o_emp_sector']
        problem_category = request.form['o_problem_category']
        counsellor_choice = request.form['o_counsellor_choice']
        counsellor = request.form['o_choose_counsellor']
        gender = request.form['o_gender']
        oemail = request.form['oemail']
        
        counsellortime = db.executeQuery(f'SELECT * FROM Available_Counsellor WHERE Name="{counsellor}"')    
        venue = counsellortime[0]
        
        curr = time.ctime()
        message = f'This is to notify you that you have booked counselling session on {curr} with {counsellor} Please come to the counselling centre at {venue[7]}. Your session is betweeen {venue[4]} to {venue[5]}. Thank You'
                
        lecMessage = f'Hello {counsellor}, Please this is to notify you that {name} has booked a counselling session with you. Thank you'
                        
        try:
            sendMail("AAMUSTED COUNSELLING CENTER",message, oemail)
            sendMail("AAMUSTED COUNSELLING CENTER",lecMessage, counsellortime[0][3])
        except Exception as e:
            return render_template('try-again.html')
            
        o_validate = db.get_oid((oid, name))
        if len(o_validate) !=0:
            db.add_others((name, phone, oid, dob, marriage, work_type, emp_sector, problem_category, counsellor_choice,counsellor, gender,oemail))
            return render_template("other-appointment-success.html") 
        else:
            return render_template("other-login-error.html") 
        
        
        
@app.route("/completed-student", methods=["POST", "GET"])
def completeStudent():
    if request.method == "GET":
        return redirect(url_for('home'))
    else:
        Sfname = request.form['sfName']
        Ssname = request.form['ssName']
        Stel = request.form['sTel']
        Semail = request.form['sEmail']
        Faculty = request.form['faculty']
        Department = request.form['sdepartment']
        sdepartment = Department
        Year = request.form['year']
        ProblemCat = request.form['problemCat']
        SpecificProblem = request.form['specificProblem']
        PreferredCounsellor = request.form['counsellorChoice']
        CounserllorType = request.form['choose_counsellor']
        Gender = request.form['gender']
        # Maritalstatus = request.form['marital-status']
        
        fullname = Sfname+" "+Ssname
        
        Choosecounsellor = []
        temp = db.get_student_based_on_counsellor(PreferredCounsellor)
        
        
        if len(temp) < 3:
            if CounserllorType == 'experience':
                ccname = db.executeQuery(f"SELECT Name FROM Available_Counsellor")
                Choosecounsellor = ccname
                print(Choosecounsellor)
            
            else:
                ccname = db.executeQuery(f"SELECT Name FROM Available_Counsellor WHERE lower(speciality) = lower('{ProblemCat}')")
                Choosecounsellor = ccname
                    
                ls=[]
                uniq =[]
                counsellorLen = getList(Choosecounsellor, ls, uniq)
                
                if(len(counsellorLen)==0):
                    return render_template("student-login-error.html")
                else:  
                    n = random.randint(0, len(counsellorLen)-1)
                    
                    PreferredCounsellor = Choosecounsellor[n][0]
                    print(PreferredCounsellor)   
                counsellortime = db.executeQuery(f'SELECT * FROM Available_Counsellor WHERE Name="{PreferredCounsellor}"')    
                venue = counsellortime[0]
                print(venue[4], venue[5])
                curr = time.ctime()
            
            message = f'This is to notify you that you have booked counselling session on {curr} with {Choosecounsellor} Please come to the counselling centre at {venue[7]}. Your session is betweeen {venue[4]} to {venue[5]}. Thank You'
                
            lecMessage = f'Hello {Choosecounsellor}, Please this is to notify you that {Sfname} {Ssname} has booked a counselling session with you. Thank you'
                        
            try:
                sendMail("AAMUSTED COUNSELLING CENTER",message, Semail)
                sendMail("AAMUSTED COUNSELLING CENTER",lecMessage, counsellortime[0][3])
            except Exception as e:
                return render_template('try-again.html')
                
            db.add_student((fullname, Stel, Faculty,sdepartment, Year, ProblemCat, SpecificProblem,CounserllorType, PreferredCounsellor, Semail, Gender))
            
            return render_template("student-appointment-success.html")
        return render_template("counsellor_limit.html")
        
                
@app.route('/counsellorlogin', methods=["POST","GET"])
def counsellorLogin():
    return render_template('consellor-login.html')

@app.route("/recorded", methods=["POST","GET"])
def recordComplete():
    if request.method == "GET":
       return redirect(url_for("home")) 
    else:
       cname = request.form['cname']
       cid = request.form['cid']
       cemail = request.form['cemail']
       counsellor_info = db.get_counsellor((cemail,cid))
       
       if len(counsellor_info) != 0:
            cphone = request.form['cphone']
            speciality = request.form['speciality']
            stime = request.form['stime']
            etime = request.form['etime']
            venue = request.form['venue']
            db.add_counsellor((cname, speciality, cphone, cemail,stime,etime,cid,venue))
            return render_template("record-counsellor-success.html")
       else:
            return render_template("record-counsellor-failed.html")
    
@app.route("/completed-lecturer", methods=["POST", "GET"])
def completeLeturer():
    if request.method == "GET":
        return redirect(url_for('home'))
    else:
        fname = request.form['lecfname']
        sname = request.form['lecsname']
        tel = request.form['lec_phone_no']
        email = request.form['lec_email']
        years = request.form['years']
        ldepartment = request.form['departments']
        problemCat = request.form['Problem Category']
        specifyProblem = request.form['Specify Problem']
        counsellorchoice = request.form['Preferred Counsellor']
        ChooseCounsellor = request.form['choose_counsellor']
        print(ChooseCounsellor)
        if counsellorchoice == 'experience':
            if problemCat.lower() == "general":
                ccname = db.executeQuery(f"SELECT Name FROM Available_Counsellor")
                
            else:
                ccname = db.executeQuery(f"SELECT Name FROM Available_Counsellor WHERE speciality = '{problemCat}'")
                ls=[]
                uniq =[]
                counsellors = getList(ccname, ls, uniq)
                
            if(len(counsellors)==0):
                return render_template('no-lecturer-available.html')
            else:  
                n = random.randint(0, len(counsellors)-1)
                ChooseCounsellor = counsellors[n]
               
                
    counsellortime = db.executeQuery(f'SELECT * FROM Available_Counsellor WHERE lower(Name)=lower("{ChooseCounsellor}")')
    print(counsellortime)     
    venue = counsellortime[0]    
    curr = time.ctime()
    
    message = f'This is to notify you that you have booked counselling session at {curr} with {ChooseCounsellor} Please come to the counselling centre at {venue[7]}.Your counselling session is between {venue[4]} to {venue[5]}. Thank You'
    lecMessage = f'Hello {ChooseCounsellor}, Please this is to notify you that {fname}+" "+ {sname} has booked a counselling session with you. Thank you'
    
        
    try:
        sendMail("AAMUSTED Counselling Centre",message, email)
        sendMail("AAMUSTED Counselling Centre",lecMessage, counsellortime[0][3]) 
    except Exception as e:
        return render_template('try-again.html')
    
    
    # gender = request.form['gender-status'] 
    fullname = fname +" "+ sname    
    db.add_lecturer((fullname, tel,email, ldepartment, years, problemCat, specifyProblem, counsellorchoice,ChooseCounsellor))
    
    return render_template("lecturer-appointment-success.html")  

@app.route("/student-login-error", methods=["GET"])
def studentLoginError():
     return redirect(url_for("newAppointment"))
 
@app.route("/lecturer-login-error", methods=["GET"])
def lecturerLoginError():
     return redirect(url_for("newAppointment"))

@app.route("/others-login-error", methods=["GET"])
def othersLoginError():
     return redirect(url_for("newAppointment"))
 
@app.route("/student-appointment-success", methods=["GET"])
def studentAppointmentSuccess():
     return redirect(url_for("home"))
 
@app.route("/lecturer-appointment-success", methods=["GET"])
def lecturerAppointmentSuccess():
     return redirect(url_for("home"))
 
@app.route("/non-registered-appointment-success", methods=["GET"])
def nonAppointmentSuccess():
     return redirect(url_for("home"))
 
@app.route("/counsellor-login-fail", methods=["GET"])
def counsellorLoginFail():
     return redirect(url_for("counsellorLogin"))
 
 
@app.route("/counsellor-login-success", methods=["GET"])
def counsellorLoginSuccess():
     return redirect(url_for("home"))




if __name__=="__main__":
    app.run(debug=True)