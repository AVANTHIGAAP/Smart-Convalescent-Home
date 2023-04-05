from flask import Flask,render_template,flash,redirect,url_for,session,g,request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,RadioField
from flask_uploads import UploadSet, configure_uploads, IMAGES
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
from functools import wraps
import email_validator

app=Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

Database_File="static/hospitalmanagement.db"

FROM_GMAIL_ADDRESS="" #use your email address
FROM_GMAIL_APP_PASSWORD="" #use your gmail app password

''' Login Form Fields '''
class LoginForm(Form):
    username = StringField('Email', [validators.Email(message='Enter valid Email'),validators.DataRequired(message="Enter an Email")])	
    password = PasswordField('Password', [validators.DataRequired(message="Enter a Password")])


'''Register Form Fields '''
class RegisterForm(Form):
	fullname = StringField('FullName', [validators.DataRequired(message="Enter your fullname")])	
	address = TextAreaField('Address', [validators.DataRequired(message="Enter your address")])
	email = StringField('Email', [validators.Email(message='Enter valid Email'),validators.DataRequired(message="Enter an Email")])
	password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords do not match')])
	confirm = PasswordField('confirm',[validators.DataRequired(message="Confirm Password")])
	contactno = StringField('Contact Number',[validators.DataRequired(message="Enter your contact number")])

class PrescriptonForm(Form):
	title=TextAreaField('Body',[validators.Length(min=10)])
	body = TextAreaField('Body',[validators.Length(min=10),validators.DataRequired(message="Please Enter Prescription Notes")])


''' Home page '''
@app.route('/')
def index():
	return render_template('home.html')

''' Register Form '''
@app.route('/register',methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		fullname = form.fullname.data
		email = form.email.data
		gender = request.form['optgender']
		date = request.form['date']
		password=form.password.data
		contactno = form.contactno.data
		address = form.address.data
		state = request.form['state']
		city = request.form['city']
		date = datetime.strptime(date, '%m/%d/%Y')
		date = date.strftime("%Y-%m-%d")
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor()
			cur.execute("select * from Users where UEmailId=?",(email,))
			data = cur.fetchone()
			if data:
				flash("Email Id already exists...Please use different Email Id",'success')
				return render_template('register.html',form=form)
			
			cur.execute("insert into Users(FullName,UAddress,Ustate,City,Gender,UEmailId,UPassword,AccountCurrentStatus,ContactNo,DOB) values(?,?,?,?,?,?,?,?,?,?)",(fullname,address,state,city,gender,email,password,'Active',contactno,date))
			cur.execute("select seq from sqlite_sequence WHERE name =?",('Users',))
			data =cur.fetchone()
			con.commit()
			link="http://127.0.0.1:5000/activate?id="+str(data[0])
			try:
				fromx = FROM_GMAIL_ADDRESS
				to  = email
				msg = MIMEText('Hi User this is the activation link please click here:\n http://127.0.0.1:5000/activate?id='+str(data[0]))
				html = """
							<html>
							  <head></head>
							  <body>
							  <b>Hi User</b><br><br>
							  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Welcome to Hospital Managment System thanks for registering inorder to activate your account please click below link <br> """+link+"""
							     
							 </body>
							</html>
							"""
				msg= MIMEText(html, 'html')
				msg['Subject'] = 'HMS............Activation Link..............'
				msg['From'] = fromx
				msg['To'] = to
				#msg.attach(part2)
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.starttls()
				server.ehlo()
				server.login(FROM_GMAIL_ADDRESS, FROM_GMAIL_APP_PASSWORD)
				server.sendmail(fromx, to, msg.as_string())
				mesg = 'Activation Link has been sent to your register mailid '+email
				server.quit()
				
			except Exception as e :
				flash('Please give the Correct Email Id','danger')
				return render_template('register.html',form=form)
			
		con.close()

		if mesg:
			flash(mesg,'success')
			return render_template('register.html',form=form)

	return render_template('register.html',form=form)

'''Activation Link '''
@app.route('/activate')
def activate():
	form = LoginForm(request.form)
	uid = request.args['id']
	with sqlite3.connect(Database_File,uri=True) as con :
		cur =con.cursor();
		cur.execute("update Users set auth=? where UserId=?",(1,uid,))
		con.commit()

	con.close()
	session['role']='16120951420'
	flash('Account has been activated......You can login now','success')
	return render_template('login.html',form = form)

	
''' Login Form '''
@app.route('/login',methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	id = request.args['role']
	session['role'] = id 
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data

		

		if id == "4153201518":
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor();
				cur.execute("select * from Doctors where DEmailID = ? AND DPassword =? ",(username,password,))
				data = cur.fetchone()
				con.commit()
			con.close()
			
			if data:
				session['doctor_login']=True
				session['doctorid']=data[0]
				session['doctorname']=data[1]
				msg="Welcome "+ data[1]
				with sqlite3.connect(Database_File) as con :
					cur =con.cursor();
					login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					cur.execute("INSERT into DoctorSessionLogs(LoginTime,DoctorId) values(?,?)",(login_time,session['doctorid'],))
					con.commit()
					cur.execute("select seq from sqlite_sequence WHERE name ='DoctorSessionLogs'")
					data = cur.fetchone()
					session['dsid']=data[0]
				con.close()
				flash(msg,'success')
				return redirect(url_for('doctor_dashboard'))
			else:
				flash("Please Enter Correct Credentails",'danger')
				return render_template('login.html',form=form,id=id)


		if id == "16120951420":
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor();
				cur.execute("select * from Users where UEmailID = ? AND UPassword =? AND AccountCurrentStatus='Active'",(username,password,))
				data = cur.fetchone()
				con.commit()
			con.close()
            	
			if data:
				if data[12] == 1:
					session['user_login']=True
					session['userid']=data[0]
					session['username']=data[1]
					msg="Welcome "+ data[1]
					with sqlite3.connect(Database_File) as con :
						cur =con.cursor();
						login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						cur.execute("INSERT into UserSessionLogs(LoginTime,UserId) values(?,?)",(login_time,session['userid'],))
						con.commit()
						cur.execute("select seq from sqlite_sequence WHERE name ='UserSessionLogs'")
						data = cur.fetchone()
						session['usid']=data[0]
					con.close()
					flash(msg,'success') 
					return redirect(url_for('user_dashboard'))
				else:
					msg="Please activate your account....An Activation Link has been sent to "+data[6]
					flash(msg,'danger')
					return render_template('login.html',form=form,id=id)
			else:
				flash("Please Enter Correct Credentails",'danger')
				return render_template('login.html',form=form,id=id)

		if id == "1413914":	
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor();
				cur.execute("select * from admin where AdminUsername = ? AND AdminPassword =?",(username,password,))
				data = cur.fetchone()
				con.commit()
			con.close()
			if data:
				session['admin_login']=True
				session['adminid']=data[0]
				msg="Welcome Admin"
				flash(msg,'success')
				return redirect(url_for('admin_dashboard'))
			else:
				flash("Please Enter Correct Credentails",'danger')
				return render_template('login.html',form=form,id=id)
	
	return render_template('login.html', form=form,id=id)

#check if user logged in
def user_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'doctor_login' in session:
			session.pop('doctor_login', None)
		if 'admin_login' in session:
			session.pop('admin_login', None)
		if 'user_login' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please login','danger')
			return redirect(url_for('index'))
	return wrap

def doctor_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'admin_login' in session:
			session.pop('admin_login', None)
		if 'user_login' in session:
			session.pop('user_login', None)
		if 'doctor_login' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please login','danger')
			return redirect(url_for('index'))
	return wrap

def admin_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'doctor_login' in session:
			session.pop('doctor_login', None)
		if 'user_login' in session:
			session.pop('user_login', None)
		if 'admin_login' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please login','danger')
			return redirect(url_for('index'))
	return wrap


'''Update_UserForm  Fields '''
class Update_UserForm(Form):
	fullname = StringField('FullName', [validators.DataRequired(message="Enter your fullname")])	
	address = TextAreaField('Address', [validators.DataRequired(message="Enter your address")])
	email = StringField('Email', [validators.Email(message='Enter valid Email'),validators.DataRequired(message="Enter an Email")])
	contactno = StringField('Cotact Number',[validators.DataRequired(message="Enter your contact number")])


'''Update_Password'''
class Update_PasswordForm(Form):
	oldpass = PasswordField('oldpass',[validators.DataRequired(message="Enter your Old Password")])
	newpass = PasswordField('newpass', [validators.DataRequired(),validators.EqualTo('confpass', message='Passwords do not match')])
	confpass = PasswordField('confpass',[validators.DataRequired(message="Confirm Password")])


'''Update User Password'''
@app.route('/update_password',methods=['GET','POST'])
@user_logged_in
def update_password():
	form = Update_PasswordForm(request.form)
	msg=""
	id="password_update"
	if request.method == 'POST' and form.validate():
		try:
			oldpass = form.oldpass.data
			newpass = form.newpass.data
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("select UPassword from Users where userid=? ",(session['userid'],))
				data = cur.fetchone()
				if str(data[0]) == str(oldpass):
					cur.execute("update Users set UPassword=? where UserId = ?",(newpass,session['userid']),)		
					msg ="Password has been updated Successfully"
					con.commit()	
				else:
					flash("Old Password does match....",'danger')
					return render_template("user_dashboard.html",form=form,id=id)
			con.close()
			if msg:
				flash(msg,'success')
				return render_template("user_dashboard.html",form=form,id=id)
				
		except Exception as e:
			flash("Something Went Wrong",'danger')
			return render_template("user_dashboard.html",form=form,id=id)
			
	return render_template("user_dashboard.html",form=form,id=id)
'''User Dashboard'''
@app.route('/user_dashboard')
@user_logged_in
def user_dashboard():
	form = Update_PasswordForm(request.form)
	id="dashboard"
	return render_template("user_dashboard.html",form=form,id=id)


'''redirect to update form '''
@app.route('/update_form')
@user_logged_in
def Update_form():
	form1 = Update_UserForm(request.form)
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor();
		cur.execute("select * from Users where userid=? ",(session['userid'],))
		data = cur.fetchone()
		con.commit()		
	con.close()


	#populate the Update_UserForm
	form1.fullname.data= data[1]
	form1.address.data = data[2]
	form1.email.data= data[6]
	form1.contactno.data =data[10]
	
	return render_template('UD_update_profile.html',form1=form1,data=data)




''' Update U'ser Form '''
@app.route('/update_userform',methods=['GET', 'POST'])
@user_logged_in
def Update_Userform():
	form1 = Update_UserForm(request.form)
	if request.method == 'POST' and form1.validate():
		try:
			fullname = form1.fullname.data
			#email = form.email.data
			gender = request.form['optgender']
			date = request.form['date']
			#password=form.password.data
			contactno = form1.contactno.data
			address = form1.address.data
			state = request.form['state']
			city = request.form['city']
			aud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("update Users set FullName=?,UAddress=?,Ustate=?,City=?,Gender=?,ContactNo=?,DOB=?,AUD=? where UserId=?",(fullname,address,state,city,gender,contactno,date,aud,session['userid'],))
				con.commit()	
			con.close()

			flash('Account Deatails has been updated','success')
			return redirect(url_for('user_dashboard'))

		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated'+e.message,'danger')
			return redirect(url_for('user_dashboard'))

	else:
		flash('Something Went wrong...Deatails are not been updated','danger')
		return redirect(url_for('user_dashboard'))

			
''' Displaying Icons  '''
@app.route('/department_page')
@user_logged_in
def department_page():
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select DeptId,DepartmentName,image_path from Departments")
		data = cur.fetchall()
		con.commit()	
	con.close()

	return render_template('departments_page.html',data =data)



list1=[]
''' Departments_Data '''
@app.route('/departments_data/<int:id>',methods=['GET','POST'])
@user_logged_in
def departments_data(id):
    form2 = Update_PasswordForm(request.form)
    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("SELECT DepartmentName,DoctorName,Fee,DoctorId from Doctors d1 join Departments d2 on d1.DeptId= d2.DeptId where d1.DeptId =?",(id,))
    	data = cur.fetchall()
    	con.commit()	
    con.close()
    
    list1.clear()

    for i in data:
    	list1.append(i)
    return redirect(url_for('appointment'))

@app.route("/appointment")
@user_logged_in
def appointment():
	return render_template("appointment_page.html",data = list1)

'''Book Appointment'''
@app.route('/book_appointment/<id>',methods=['GET','POST'])
@user_logged_in
def book_appointment(id):
	form2 = Update_PasswordForm(request.form)
	app_date=request.form["date"]
	app_date=datetime.strptime(app_date,"%d/%m/%Y")
	app_date=app_date.strftime("%d-%b-%Y")
	app_time=request.form["time"]
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select DepartmentName from Departments d1 JOIN Doctors d2 on d1.DeptId = d2.DeptId where DoctorId = ?",(id,))
		data = cur.fetchone()
		cur.execute("INSERT into Appointments(AppDate,APPTime,UserId,DoctorId,Department) VALUES(?,?,?,?,?)",(app_date,app_time,session["userid"],id,data[0],))
		con.commit()
		msg="Appointment has Successfully booked...you can view it in Appointment History"	
	con.close()
	if msg:
		flash(msg,'success')
		return redirect(url_for('user_dashboard'))
	else:
		flash("Something went wrong",'danger')
		return redirect(url_for("department_page"))

''' Appointment History'''
@app.route('/appointment_history',methods=['GET','POST'])
@user_logged_in
def appointment_history():

    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select DoctorName,Department,Fee,APPTime,AppDate,AppointmentStatus,AppointmentNo from Doctors as doc JOIN Appointments as app on doc.DoctorId =app.DoctorId where UserId=? and AppointmentStatus=?",(session['userid'],'Active',))
    	data = cur.fetchall()
    	con.commit()	
    con.close()

    list1.clear()

    if data:
    	mesg=""
    else:
        flash("No appointment has booked by you... Please Click on Book Appointment to confirm your slot",'success')
        return redirect(url_for('appointment_list'))
        
    for i in data:
    	list1.append(i)
    return redirect(url_for('appointment_list'))

@app.route("/appointment_list")
@user_logged_in
def appointment_list():
	return render_template("appointment_history.html",data = list1)

''' Deleting appointment'''
@app.route("/delete_appointment/<aptid>")
@user_logged_in
def delete_appointment(aptid):
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("update Appointments set AppointmentStatus=?,AdminRefereceStatus=? where AppointmentNo=? ",('Inactive','Cancled by patient',aptid,))
		con.commit()	
	con.close()
	flash('Appointment has been Cancled','danger')
	return redirect(url_for("appointment_history"))



@app.route("/view_prescrptions")
@user_logged_in
def view_prescrptions():
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select * from prescription where UserId=?",(session['userid'],))
		data=cur.fetchall()
		con.commit()	
	con.close()
	
	list1.clear()
	for i in data:
		list1.append(list(i))
	
	count=0
	for i in range(len(list1)):
		count=count+1
		list1[i].append(count)

	return redirect(url_for('view_prescrptions_copy'))
	

@app.route("/view_prescrptions_copy")
@user_logged_in
def view_prescrptions_copy():
	return render_template("view_prescription.html",data=list1)



@app.route("/display_prescription/<id>")
@user_logged_in
def display_prescription(id):
	form=PrescriptonForm(request.form)
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select pdata from prescription where pid=?",(id,))
		data=cur.fetchone()
		con.commit()	
	con.close()
	
	#form.body.data=data[0]
	return render_template("display_prescription.html",data=data)






#------------------------------------------DOCTOR DASHBOARD ----------------------------------------#





@app.route('/doctor/doctor_dashboard')
@doctor_logged_in
def doctor_dashboard():
	form = Update_PasswordForm(request.form)
	id="dashboard"
	return render_template('doctor/doctor_dashboard.html',form = form,id=id)

'''Update_DoctorForm  Fields '''
class Update_DoctorForm(Form):
	doctorname = StringField('DoctorName', [validators.DataRequired(message="Enter your fullname")])	
	address = TextAreaField('DoctorAddress', [validators.DataRequired(message="Enter your address")])
	contactno = StringField('Cotact Number',[validators.DataRequired(message="Enter your contact number")])
	fee = StringField('Consultancy Fee',[validators.DataRequired(message="Please Enter Consultancy Fee")])
	newpass = PasswordField('newpass', [validators.DataRequired(),validators.EqualTo('confpass', message='Passwords do not match')])
	confpass = PasswordField('confpass',[validators.DataRequired(message="Confirm Password")])

	
'''Populating Data'''
@app.route('/doctor/update_doctorform')
@doctor_logged_in
def Update_doctorform():
	form = Update_DoctorForm(request.form)
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor();
		cur.execute("select DeptId,DoctorName,Fee,DContactNo,DEmailID,DAddress,dstate,dcity from Doctors where DoctorId=?",(session['doctorid'],))
		data = cur.fetchone()
		cur.execute("select * from Departments")
		departments_data = cur.fetchall()
		con.commit()		
	con.close()


	#populate the Update_DoctorForm
	form.doctorname.data= data[1]
	form.fee.data= data[2]
	form.address.data = data[5]
	form.contactno.data =data[3]
	
	return render_template('doctor/DD_update_profile.html',form=form,data=data,departments_data=departments_data)


''' Update Doctor Profile  '''
@app.route('/doctor/update_doctorprofile',methods=['GET', 'POST'])
@doctor_logged_in
def update_doctorprofile():
	form = Update_DoctorForm(request.form)
	if request.method == 'POST':
		try:
			department_id=request.form['department_id']
			doctorname = form.doctorname.data
			fee = form.fee.data
			#password=form.password.data
			contactno = form.contactno.data
			address = form.address.data
			state = request.form['state']
			city = request.form['city']
			aud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("update Doctors set DoctorName=?,Fee=?,DAddress=?,DeptId=?,dstate=?,dcity=?,DContactNo=?,DAUD=? where DoctorId=?",(doctorname,fee,address,department_id,state,city,contactno,aud,session['doctorid'],))
				con.commit()	
			con.close()

			flash('Account Deatails has been updated','success')
		
			return redirect(url_for('doctor_dashboard'))
		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated'+e.message,'danger')
			return redirect(url_for('doctor_dashboard'))

	else:
		flash('Something Went wrong...Deatails are not been updated','danger')
		return redirect(url_for('doctor_dashboard'))

list2=[]

''' Appointment history of doctor '''

@app.route('/doctor/doctor_appointments',methods=['GET','POST'])
@doctor_logged_in
def doctor_appointments():

    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select a.AppointmentNo,u.FullName,a.AppDate,a.AppTime,a.AppointmentStatus,a.Department from Appointments a join Users u on a.UserId = u.UserId where DoctorId = ? and AppointmentStatus=?",(session['doctorid'],'Active'))
    	data = cur.fetchall()
    	con.commit()	
    con.close()

    list1.clear()

    if data:
    	mesg=""
    else:
        flash("There are no appointments to check.....",'success')
        return redirect(url_for('doctor_appointment_list'))
        
    for i in data:
    	list1.append(i)

    return redirect(url_for('doctor_appointment_list'))

@app.route("/doctor_appointment_list")
@doctor_logged_in
def doctor_appointment_list():
	return render_template("doctor/appointment_history.html",data = list1)

@app.route("/doctor/delete_appointment/<aptid>/<reason>")
@doctor_logged_in
def doctor_delete_appointment(aptid,reason):
	with sqlite3.connect(Database_File) as con :
		try:
			cur =con.cursor()
			cur.execute("update Appointments set AppointmentStatus=?,AdminRefereceStatus=? where AppointmentNo=? ",('Inactive','Cancled by doctor',aptid,))
			cur.execute("select UEmailId from Users where UserId=(select UserId from Appointments WHERE AppointmentNo=?)",(aptid,))
			data=cur.fetchone()
			fromx = FROM_GMAIL_ADDRESS  
			to  =  str(data[0])
			msg = MIMEText('Hi User,\n Sorry to say your appointment has been Cancled by doctor\nReason is:\n\t\t'+reason)
			msg['Subject'] = 'HMS........Appointment Cancellation...............'
			msg['From'] = fromx
			msg['To'] = to
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.ehlo()
			server.login(FROM_GMAIL_ADDRESS, FROM_GMAIL_APP_PASSWORD)
			server.sendmail(fromx, to, msg.as_string())
			server.quit()
			con.commit()
		except Exception as e :
			flash('Error Message'+str(e),'danger')
			return redirect(url_for("doctor_appointments"))	
	con.close()
	flash('Appointment has been Cancled','danger')
	return redirect(url_for("doctor_appointments"))

'''Update Doctor Password'''
@app.route('/update_dpassword',methods=['GET','POST'])
@doctor_logged_in
def update_dpassword():
	form = Update_PasswordForm(request.form)
	id="password_update"
	msg=""
	if request.method == 'POST' and form.validate():
		try:
			oldpass = form.oldpass.data
			newpass = form.newpass.data
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("select DPassword from Doctors where DoctorId=? ",(session['doctorid'],))
				data = cur.fetchone()
				if str(data[0]) == str(oldpass):
					cur.execute("update Doctors set DPassword=? where DoctorId = ?",(newpass,session['doctorid']),)		
					msg ="Password has been updated Successfully"
					con.commit()	
				else:
					flash("Old Password does match....",'danger')
					return render_template('doctor/doctor_dashboard.html',form = form,id=id)
			con.close()
			if msg:
				flash(msg,'success')
				return render_template('doctor/doctor_dashboard.html',form = form,id=id)
				
		except Exception as e:
			flash("Something Went Wrong",'danger')
			return render_template('doctor/doctor_dashboard.html',form = form,id=id)

	return render_template('doctor/doctor_dashboard.html',form = form,id=id)


@app.route('/prescription/<id>',methods=["GET","POST"])
@doctor_logged_in
def prescription(id):
	form=PrescriptonForm(request.form)
	#form = Update_PasswordForm(request.form)
	with sqlite3.connect(Database_File) as con:
		cur=con.cursor()
		cur.execute("select UserId,DoctorId FROM Appointments where AppointmentNo=?",(id,))
		data=cur.fetchone()
		cur.execute("select * from Users where UserId=?",(int(data[0]),))
		user_data=cur.fetchone()
		cur.execute("SELECT (strftime('%Y', 'now') - strftime('%Y', DOB)) - (strftime('%m-%d', 'now') < strftime('%m-%d',DOB))  from Users where UserId=?",(int(data[0]),))
		age=cur.fetchone()
		cur.execute("select * from Doctors where DoctorId=?",(int(data[1]),))
		doctor_data=cur.fetchone()
		cur.execute("select DepartmentName from Doctors d1 join Departments d2 on d1.DeptId = d2.DeptId where DoctorId=?",(int(doctor_data[0]),))
		dept_name=cur.fetchone()
		con.commit()
	con.close()


	if request.method == "POST":
		with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				body=form.body.data
				cur.execute("select UserId,DoctorId FROM Appointments where AppointmentNo=?",(id,))
				data=cur.fetchone()
				cur.execute("insert into prescription(pdata,UserId,DoctorId,Username,DoctorName,DepartmentName) values(?,?,?,?,?,?)",(body,data[0],data[1],user_data[1],doctor_data[1],dept_name[0],))
				con.commit()
				cur =con.cursor()
				cur.execute("update Appointments set AppointmentStatus=?, AdminRefereceStatus=? where AppointmentNo=?",('Inactive','Prescription Given',id,))
				con.commit()
				flash('Prescription Note has been shared','success')
				return redirect(url_for("doctor_appointments"))
				
		con.close()

	return render_template("/doctor/prescription.html",form=form,id=id,user_data=user_data,doctor_data=doctor_data,dept_name=dept_name,age=age)


@app.route("/prescription_history")
@doctor_logged_in
def prescription_history():
	with sqlite3.connect(Database_File) as con:
		cur=con.cursor()
		cur.execute("select * from prescription where DoctorId=?",(session['doctorid'],))
		data=cur.fetchall()
		con.commit()
	con.close()

	l=[]
	for i in data:
		l.append(list(i))

	count=0
	for i in range(len(l)):
		count=count+1
		l[i].append(count)


	return render_template("/doctor/prescription_history.html",data=l)

@app.route("/view_prescrption_note/<id>")
@doctor_logged_in
def view_prescription_note(id):
	with sqlite3.connect(Database_File) as con:
		cur=con.cursor()
		cur.execute("select pdata from prescription where pid=?",(id,))
		data=cur.fetchone()
		con.commit()
	con.close
	return render_template("/doctor/display_prescription.html",data=data)





#-----------------------------------------------------ADMIN DASHBOARD------------------------------------#



''' admin dashboard '''
@app.route('/admin_dashboard')
@admin_logged_in
def admin_dashboard():
	form = Update_PasswordForm(request.form)
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select count(*) from Users where AccountCurrentStatus='Active'")
		patients_count= cur.fetchone()[0]
		cur.execute("select count(*) from Doctors where DAccountStatus='Active'")
		doctors_count=cur.fetchone()[0]
		cur.execute("select count(*) from Appointments where AppointmentStatus='Active'")
		appointment_count=cur.fetchone()[0]
		list1=[]
		list1=[patients_count,doctors_count,appointment_count]

	con.close()
	
	return render_template('admin/admin_dashboard.html',form = form,list1=list1,id="dashboard")

''' Mange Patients '''
@app.route('/manage_patients',methods=['GET','POST'])
@admin_logged_in
def manage_patients():
    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select * from Users where AccountCurrentStatus='Active'")
    	data = cur.fetchall()
    	con.commit()	
    con.close()
    list1.clear()
    if data:
    	mesg=""
    else:
        flash("There are no Users.....",'success')
        return render_template("/admin/manage_patients.html",data = list1)

    for i in data:
    	list1.append(list(i))

    for i in range(len(list1)):
    	list1[i][2]=list1[i][2]+","+list1[i][4]+","+list1[i][3]
    	if list1[i][9] is None:
    		list1[i][9]=""

    return redirect(url_for('manage_patients_copy'))

@app.route("/manage_patients_copy")
@admin_logged_in
def manage_patients_copy():
	return render_template("/admin/manage_patients.html",data = list1)


@app.route('/delete_user/<duid>')
@admin_logged_in
def delete_user(duid):
	try:
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor()
			cur.execute("update Users set AccountCurrentStatus='Inactive' where UserId=?",(duid,))
			con.commit()	
		con.close()
		flash('Account has been deleted','danger')
		return redirect(url_for('manage_patients'))
	except Exception as e:
		flash('Something Went Wrong User account has been not deleted...Error: '+str(e),'danger')
		return redirect(url_for('manage_patients'))

@app.route('/manage_doctors',methods=['GET','POST'])
@admin_logged_in
def manage_doctors():

    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select DoctorId,DepartmentName,DoctorName,DAccountCD from Doctors d1 JOIN Departments d2 on d1.DeptId=d2.DeptId where DAccountStatus='Active'")
    	data = cur.fetchall()
    	con.commit()	
    con.close()
    
    list1.clear()

    if data:
    	mesg=""
    else:
        flash("There are no Doctors.....",'success')
        return redirect(url_for('manage_doctors_copy'))

    for i in data:
    	list1.append(list(i))

    return redirect(url_for('manage_doctors_copy'))

@app.route("/manage_doctors_copy")
@admin_logged_in
def manage_doctors_copy():
	return render_template('/admin/manage_doctors.html',data = list1)



@app.route("/delete_doctor/<ddid>")
@admin_logged_in
def delete_doctor(ddid):
	try:
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor()
			cur.execute("update Doctors set DAccountStatus='Inactive' where DoctorId=?",(ddid,))
			con.commit()	
		con.close()
		flash('Account has been deleted','danger')
		return redirect(url_for('manage_doctors'))
	except Exception as e:
		flash('Something Went Wrong User account has been not deleted...Error: '+str(e),'danger')
		return redirect(url_for('manage_doctors'))



@app.route('/add_doctor',methods=['GET','POST'])
@admin_logged_in
def add_doctor():
	form = Update_DoctorForm(request.form)
	form_action="/add_doctor"
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select * from Departments")
		departments_data = cur.fetchall()
		con.commit()	
	con.close()
	if request.method == 'POST' and form.validate():
		try:
			department_id=request.form['department_id']
			doctorname = form.doctorname.data
			fee = form.fee.data
			email=request.form['email']
			password=form.newpass.data
			contactno = form.contactno.data
			address = form.address.data
			state = request.form['state']
			city = request.form['city']
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("insert into Doctors(DoctorName,Fee,DAddress,DEmailID,DPassword,DeptId,auth,dstate,dcity,DContactNo,DAccountStatus) VALUES(?,?,?,?,?,?,?,?,?,?,'Active')",(doctorname,fee,address,email,password,department_id,1,state,city,contactno,))
				con.commit()	
			con.close()
			flash('Record has been inserted','success')
			return render_template('/admin/add_doctor.html',form=form,form_action=form_action,data=None,title='Add',departments_data=departments_data)

		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated '+str(e),'danger')
			return render_template('/admin/add_doctor.html',form=form,form_action=form_action,data=None,title='Add',departments_data=departments_data)
	


	return render_template('/admin/add_doctor.html',form=form,form_action=form_action,data=None,title="Add",departments_data=departments_data)




@app.route('/edit_doctor/<id>',methods=['GET','POST'])
@admin_logged_in
def edit_doctor(id):
	form = Update_DoctorForm(request.form)
	form_action="/edit_doctor/"+id

	if request.method == 'POST':
		try:
			department_id=request.form['department_id']
			doctorname = form.doctorname.data
			fee = form.fee.data
			#password=form.password.data
			contactno = form.contactno.data
			address = form.address.data
			state = request.form['state']
			city = request.form['city']
			aud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("update Doctors set DoctorName=?,Fee=?,DAddress=?,DeptId=?,dstate=?,dcity=?,DContactNo=?,DAUD=? where DoctorId=?",(doctorname,fee,address,department_id,state,city,contactno,aud,id,))
				con.commit()	
			con.close()

			flash('Account Deatails has been updated','success')
		
			return redirect(url_for('manage_doctors'))
		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated'+e.message,'danger')
			return redirect(url_for('manage_doctors'))


	with sqlite3.connect(Database_File) as con :
		cur =con.cursor();
		cur.execute("select DeptId,DoctorName,Fee,DContactNo,DEmailID,DAddress,dstate,dcity from Doctors where DoctorId=?",(id,))
		data = cur.fetchone()
		cur.execute("select * from Departments")
		departments_data = cur.fetchall()
		con.commit()		
	con.close()

	
	list1.clear()
	list2.clear()

	for i in data:
		list1.append(i)
	list1.append(form_action)

	for i in departments_data:
		list2.append(i)
	
	return redirect(url_for('edit_doctor_copy'))

@app.route('/edit_doctor_copy')
@admin_logged_in
def edit_doctor_copy():
	form=Update_DoctorForm(request.form)
	form.doctorname.data= list1[1]
	form.fee.data= list1[2]
	form.address.data = list1[5]
	form.contactno.data =list1[3]
	return render_template("/admin/add_doctor.html",form=form,data=list1,departments_data=list2,form_action=list1[-1],title='Edit')


@app.route('/manage_appointments',methods=['GET','POST'])
@admin_logged_in
def manage_appointments():
    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select DoctorName,FullName,Department,Fee,AppDate,APPTime,AppointmentCD,AdminRefereceStatus from Appointments a join Doctors d on a.DoctorId=d.DoctorId JOIN Users u on u.UserId = a.UserId")
    	data = cur.fetchall()
    	con.commit()	
    con.close()
    list1.clear()
    if data:
    	mesg=""
    else:
        flash("There are no Appointments.....",'success')
        t=()
        return render_template("/admin/manage_appointments.html",data = t)

    for i in data:
    	list1.append(list(i))

    for i in range(len(list1)):
    	list1[i][4]=list1[i][4]+"/"+list1[i][5]
    	if list1[i][7]:
    		list1[i].append("Inactive")
    	else:
    		list1[i][7]="Active"
    		list1[i].append("")
    		
    	#i=0
    	#i=i+list1	
    return redirect(url_for('manage_appointments_copy'))

@app.route("/manage_appointments_copy")
@admin_logged_in
def manage_appointments_copy():
	return render_template("/admin/manage_appointments.html",data = list1)


@app.route('/add_department', methods=['GET', 'POST'])
@admin_logged_in
def add_department():
    if request.method == 'POST' and 'photo' in request.files:
    	department_name = request.form['department_name']
    	filename = photos.save(request.files['photo'])
    	with sqlite3.connect(Database_File) as con :
    		cur =con.cursor()
    		cur.execute("insert into Departments(DepartmentName,image_path) values(?,?)",(department_name,filename,))
    		con.commit()	
    	con.close()
    	flash('Department has been Added','success')
    	return redirect(url_for('manage_departments'))
    return render_template('admin/add_department.html')


@app.route('/manage_departments',methods=['GET','POST'])
@admin_logged_in
def manage_departments():
    with sqlite3.connect(Database_File) as con :
    	cur =con.cursor()
    	cur.execute("select * from Departments")
    	data = cur.fetchall()
    	con.commit()	
    con.close()
    list1.clear()
    if data:
    	mesg=""
    else:
        flash("There are no Departments.....",'success')
        return redirect(url_for('manage_departments'))

    for i in data:
    	list1.append(list(i))

    count=0
    for i in range(len(list1)):
    	count=count+1
    	list1[i].append(count)


    return redirect(url_for('manage_departments_copy'))

@app.route("/manage_departments_copy")
@admin_logged_in
def manage_departments_copy():
	return render_template("/admin/manage_departments.html",data = list1)

@app.route('/doctor/upload', methods=['GET', 'POST'])
@admin_logged_in
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        with sqlite3.connect(Database_File) as con :
        	cur =con.cursor()
        	cur.execute("insert into filenames(filename) values(?)",(filename,))
        	con.commit()	
        con.close()
    return render_template('doctor/upload.html')
 


@app.route("/delete_department/<id>")
@admin_logged_in
def delete_department(id):
	try:
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor()
			cur.execute("select image_path from Departments where DeptId=?",(id,))
			data=cur.fetchone()
			cur.execute("delete from Departments where DeptId=?",(id,))
			os.remove("static/images/"+data[0])
			con.commit()	
		con.close()
		flash('Department has been deleted','danger')
		return redirect(url_for('manage_departments'))
	except Exception as e:
		flash('Something Went Wrong  Department has been not deleted...Error: '+str(e),'danger')
		return redirect(url_for('manage_departments'))



@app.route("/DoctorSessionLogs")
@admin_logged_in
def DoctorSessionLogs():
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor();
		cur.execute("select d1.DoctorId,DEmailID,LoginTime,Logout  from DoctorSessionLogs d1 join Doctors d2 on d1.DoctorId=d2.DoctorId ")
		data =cur.fetchall()
		con.commit()
	con.close()
	list1.clear()
	for i in data:
		list1.append(list(i))

	for i in range(len(list1)):
		if list1[i][2] and list1[i][3] :
			list1[i].append("Success")
		else:
			list1[i][3]=""
			list1[i].append("Failed")
	count=0
	for i in range(len(list1)):
		count=count+1
		list1[i].append(count)

	return redirect(url_for('doctorsessionlogs_copy'))

@app.route('/doctorsessionlogs_copy')
@admin_logged_in
def doctorsessionlogs_copy():
	return render_template("/admin/doctorsessionlogs.html",data=list1)


@app.route("/UserSessionLogs")
@admin_logged_in
def UserSessionLogs():
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor();
		cur.execute("select u1.UserId,UEmailId,LoginTime,Logout from UserSessionLogs u1 join Users u2 where u1.UserId=u2.UserId")
		data =cur.fetchall()
		con.commit()
	con.close()
	list1.clear()
	for i in data:
		list1.append(list(i))

	for i in range(len(list1)):
		if list1[i][2] and list1[i][3] :
			list1[i].append("Success")
		else:
			list1[i][3]=""
			list1[i].append("Failed")
	count=0
	for i in range(len(list1)):
		count=count+1
		list1[i].append(count)

	return redirect(url_for('usersessionlogs_copy'))

@app.route('/usersessionlogs_copy')
@admin_logged_in
def usersessionlogs_copy():
	return render_template("/admin/usersessionlogs.html",data=list1)



@app.route("/contactus_list")
@admin_logged_in
def contactus_list():
	with sqlite3.connect(Database_File) as con:
		cur=con.cursor()
		cur.execute("select * from contactus")
		data=cur.fetchall()
		con.commit()
	con.close()
	list1.clear()
	count=0
	for i in data:
		list1.append(list(i))
	for i in range(len(data)):
		count=count+1
		list1[i].append(count)

	return render_template("/admin/contactus.html",data=list1)

@app.route('/delete_comment/<id>')
@admin_logged_in
def delete_comment(id):
	with sqlite3.connect(Database_File) as con:
		cur=con.cursor()
		cur.execute("delete from contactus where cid=?",(id,))
		con.commit()
	con.close()
	return redirect(url_for("contactus_list"))




@app.route('/admin_password_update',methods=['GET','POST'])
@admin_logged_in
def admin_password_update():
	form = Update_PasswordForm(request.form)
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select count(*) from Users where AccountCurrentStatus='Active'")
		patients_count= cur.fetchone()[0]
		cur.execute("select count(*) from Doctors where DAccountStatus='Active'")
		doctors_count=cur.fetchone()[0]
		cur.execute("select count(*) from Appointments where AppointmentStatus='Active'")
		appointment_count=cur.fetchone()[0]
		list1=[]
		list1=[patients_count,doctors_count,appointment_count]

	con.close()
	
	
	msg=""
	if request.method == 'POST' and form.validate():
		try:
			oldpass = form.oldpass.data
			newpass = form.newpass.data
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("select AdminPassword from admin where AdminNo=? ",(session['adminid'],))
				data = cur.fetchone()
				if str(data[0]) == str(oldpass):
					cur.execute("update admin set AdminPassword=? where AdminNo = ?",(newpass,session['adminid']),)		
					msg ="Password has been updated Successfully"
					con.commit()	
				else:
					flash("Old Password does match....",'danger')

					return render_template('admin/admin_dashboard.html',form = form,list1=list1,id="password_update")
			con.close()
			if msg:
				flash(msg,'success')
				return render_template('admin/admin_dashboard.html',form = form,list1=list1,id="password_update")
				
		except Exception as e:
			flash("Something Went Wrong",'danger')
			return render_template('admin/admin_dashboard.html',form = form,list1=list1,id="password_update")

	return render_template('admin/admin_dashboard.html',form = form,list1=list1,id="password_update")



@app.route('/logout')
def logout():
	form = LoginForm(request.form)
	id=session['role']
	#session.pop('role', None)
	
	if id == "4153201518":
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor();
			logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			cur.execute("Update DoctorSessionLogs set Logout=? WHERE DSid=?",(logout_time,session['dsid'],))
			con.commit()
			session.pop('doctor_login', None)
		con.close()
	if id == "16120951420":
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor();
			logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			cur.execute("Update UserSessionLogs set Logout=? WHERE USid=?",(logout_time,session['usid'],))
			con.commit()
			session.pop('user_login', None)
		con.close()

	if id == "1413914":
		session.pop('admin_login', None)

	flash('you have successfully logout','success')
	return render_template('login.html',form=form,id=id)





#--------------------------------------------Normal Pages-------------------------------------------------#




@app.route('/forget/<id>',methods=['GET','POST'])
def forget(id):
	session['role']=id
	if request.method == 'POST':	
		email=request.form['email']
		contactno=request.form['contactno']
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor();
			if session['role'] == "16120951420":
				cur.execute("select UserId from Users where UEmailId=? and ContactNo=?",(email,contactno,))
				data = cur.fetchone()
			elif session['role'] == "4153201518":
				cur.execute("select DoctorId from Doctors where DEmailId=? and DContactNo=?",(email,contactno,))
				data = cur.fetchone()
			elif session['role'] == "1413914":
				cur.execute("select AdminNo from admin where AdminUsername=? and AdminContact=?",(email,contactno,))
				data = cur.fetchone()
			con.commit()
		con.close()
		try:
			
			link="http://127.0.0.1:5000/forget_password/"+str(data[0])
			fromx = FROM_GMAIL_ADDRESS
			to  = email
			html = """
							<html>
							  <head></head>
							  <body>
							  <b>Hi User</b><br> 
							  This is the activation link please <br> """+link+"""
							     
							 </body>
							</html>
							"""
				
			msg= MIMEText(html, 'html')
			msg['Subject'] = 'HMS..............Account Recovery Link...............'
			msg['From'] = fromx
			msg['To'] = to
			#msg.attach(part2)
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.ehlo()
			server.login(FROM_GMAIL_ADDRESS, FROM_GMAIL_APP_PASSWORD)
			server.sendmail(fromx, to, msg.as_string())
			mesg = 'Account Recovery Link has been sent to your register mailid '+email
			server.quit()
			flash(mesg,'success')
			return render_template('forget_password.html')

		except Exception as e:
			flash('Give Correct input.....','danger')
			return render_template('forget_password.html')

		
	return render_template('forget_password.html')


@app.route('/forget_password/<id>',methods=['GET','POST'])
def forget_password(id):
	form1 = Update_PasswordForm(request.form)
	form = LoginForm(request.form)
	session['update_id']=id
	if request.method == 'POST':
		password=form1.newpass.data
		with sqlite3.connect(Database_File) as con :
			cur =con.cursor()
			if session['role'] == "16120951420":
				cur.execute("update Users set UPassword=? where UserId=?",(password,id,))
				data=cur.fetchone()
			elif session['role'] == "4153201518":
				cur.execute("update Doctors set DPassword=? where DoctorId=?",(password,id,))
				data=cur.fetchone()
			elif session['role'] == "1413914":
				cur.execute("update admin set AdminPassword=? where AdminNo=?",(password,id,))
				data=cur.fetchone()
			con.commit()	
		con.close()
		flash('Password has been changed...Please login','success')
		return render_template('login.html',form=form,id=id)
		
	return render_template('update_password.html',form1 = form1,id=id)


@app.route('/contactus',methods=['GET','POST'])
def contactus():
	if request.method == 'POST':
		name=request.form['name']
		email=request.form['email']
		comment=request.form['comment']
		with sqlite3.connect(Database_File) as con:
			cur=con.cursor()
			cur.execute("insert into contactus(name,email,comment) values(?,?,?)",(name,email,comment,))
			con.commit()
		con.close()
		flash("Thanks for contacting us ...we will contact you with in 24 hrs","success")
		return render_template("home.html")



@app.route('/test/<id>',methods=['GET','POST'])
def test(id):
	with sqlite3.connect(Database_File) as con :
		cur =con.cursor()
		cur.execute("select * from test where testid=?",(id,))
		data=cur.fetchone()
		con.commit()	
	con.close()
	form_action="/test/"+id
	if request.method == 'POST':
		try:
			testname = request.form['testname']
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("update test set Testname=? where testid=?",(testname,id,))
				con.commit()	
			con.close()

			flash('Account Deatails has been updated','success')
		
			return render_template('/admin/add_doctor.html',data=None)
		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated'+e.message,'danger')
			return render_template('/admin/add_doctor.html',data=None)


	
	return render_template('/admin/add_doctor.html',form_action=form_action,data=data)




@app.route('/test',methods=['GET','POST'])
def test_add():
	form_action="/test"

	if request.method == 'POST' :
		try:
			testname = request.form['testname']
			with sqlite3.connect(Database_File) as con :
				cur =con.cursor()
				cur.execute("insert into test(Testname) values(?)",(testname,))
				con.commit()	
			con.close()

			flash('Record has been inserted','success')
		
			return render_template('/admin/add_doctor.html',form_action=form_action,data=None)
		except Exception as e :
			flash('Something Went wrong...Deatails are not been updated '+str(e),'danger')
			return render_template('/admin/add_doctor.html',form_action=form_action,data=None)
	
	return render_template('/admin/add_doctor.html',form_action=form_action,data=None)


if __name__ == '__main__':
	app.secret_key='1234567'
	app.run(debug=True)