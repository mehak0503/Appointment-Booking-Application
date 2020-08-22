import tkinter as tk 
from tkinter import ttk,messagebox 
from db import *
from tkcalendar import Calendar, DateEntry
import datetime

#Main Application
class tkinterApp(tk.Tk): 
	
	# __init__ function for class tkinterApp 
	def __init__(self, *args, **kwargs): 
		
		# __init__ function for class Tk 
		tk.Tk.__init__(self, *args, **kwargs) 
		tk.Tk.title(self,"Appointment Booking Application")		
		# creating a container 
		container = tk.Frame(self) 
		container.pack(side = "top", fill = "both", expand = True) 

		container.grid_rowconfigure(0, weight = 1) 
		container.grid_columnconfigure(0, weight = 1) 
		self.container = container
		# initializing frames to an empty array 
		self.frames = {} 

		# iterating through a tuple consisting 
		# of the different page layouts 
		for klass in (LoginForm, RegistrationForm, AppointmentForm,BookedForm):
			self.frames[klass.__name__] = klass(container, self)
			self.frames[klass.__name__].grid(row = 0, column=0,sticky="nsew")

			# initializing frame of that object from 
			# LoginForm, RegistrationForm, AppointmentForm respectively with 
			# for loop 
			self.frames["LoginForm"].tkraise() 
	
# first window frame LoginForm 
class LoginForm(tk.Frame): 
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.username=None
		self.userid = None
		textLabel = tk.Label(self, text="Login Form")
		textLabel.grid(row=0, column=1,padx = 40, pady = 10)
		nameLabel = tk.Label(self, text="Username:")
		nameLabel.grid(row=1, column=0,padx = 10, pady = 10)
		self.name = tk.Entry(self, width=30)
		self.name.grid(row=1, column=1,padx = 10, pady = 10)
		passLabel = tk.Label(self, text="Password:")
		passLabel.grid(row=2, column=0,padx = 10, pady = 10)
		self.password = tk.Entry(self, width=30,show="*")
		self.password.grid(row=2, column=1,padx = 10, pady = 10)
		childFrame = tk.Frame(self,relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
		childFrame.grid(row = 3, column = 1)
		loginButton = ttk.Button(childFrame, text ="Login", 
		command = lambda: self.login(self.name.get(),self.password.get(),controller)) 
		loginButton.grid(row = 0, column = 0, padx = 5, pady = 5)  
		registerButton = ttk.Button(childFrame, text ="Register", 
		command = lambda : controller.frames["RegistrationForm"].tkraise()) 
		registerButton.grid(row = 0, column = 1, padx = 5, pady = 5) 

	#Process login details
	def login(self,name,password,controller):
		params = []
		params.append(name)
		params.append(password)
		sql = "SELECT password FROM users WHERE username=?"
		rows = get_records(sql,tuple([params[0]]))
		if len(rows)<=0:
			messagebox.showinfo("Login Failed", "User not found!")
			controller.frames["RegistrationForm"].tkraise()
		elif str(rows[0][0])!=params[1]:
			messagebox.showinfo("Login Failed", "Incorrect password!")
			controller.frames["RegistrationForm"].tkraise()
		else:
			self.username = name
			sql = "SELECT userid FROM users WHERE username=?"
			res = get_records(sql,tuple([name]))
			self.userid = res[0][0]
			controller.frames["AppointmentForm"].tkraise_()
		
	#Reset username on logout
	def tkraise(self):
		self.name.delete(0,'end')
		self.password.delete(0,'end')
		tk.Frame.tkraise(self)


# second window frame RegistrationForm 
class RegistrationForm(tk.Frame): 
	
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 
		self.username=None
		self.userid = None
		textLabel = tk.Label(self, text="Registration Form")
		textLabel.grid(row=0, column=1,padx = 40, pady = 10)
		nameLabel = tk.Label(self, text="Username:")
		nameLabel.grid(row=1, column=0,padx = 5, pady = 5)
		name = tk.Entry(self, width=30)
		name.grid(row=1, column=1,padx = 5, pady = 5)
		passLabel = tk.Label(self, text="Password:")
		passLabel.grid(row=2, column=0,padx = 5, pady = 5)
		password = tk.Entry(self, width=30,show="*")
		password.grid(row=2, column=1,padx = 5, pady = 5)
		fnameLabel = tk.Label(self, text="Firstname:")
		fnameLabel.grid(row=3, column=0,padx = 5, pady = 5)
		fname = tk.Entry(self, width=30)
		fname.grid(row=3, column=1,padx = 5, pady = 5)
		lnameLabel = tk.Label(self, text="Lastname:")
		lnameLabel.grid(row=4, column=0,padx = 5, pady = 5)
		lname = tk.Entry(self, width=30)
		lname.grid(row=4, column=1,padx = 5, pady = 5)
		cityLabel = tk.Label(self, text="City:")
		cityLabel.grid(row=5, column=0,padx = 5, pady = 5)
		city = tk.Entry(self, width=30)
		city.grid(row=5, column=1,padx = 5, pady = 5)
		addressLabel = tk.Label(self, text="Address:")
		addressLabel.grid(row=6, column=0,padx = 5, pady = 5)
		address = tk.Entry(self, width=30)
		address.grid(row=6, column=1,padx = 5, pady = 5)
		ageLabel = tk.Label(self, text="Age:")
		ageLabel.grid(row=7, column=0,padx = 5, pady = 5)
		age = tk.Entry(self, width=30)
		age.grid(row=7, column=1,padx = 5, pady = 5)
		genderLabel = tk.Label(self, text="Gender:")
		genderLabel.grid(row=8, column=0,padx = 5, pady = 5)
		gender = tk.StringVar()
		gender.set('M')
		genderM = tk.Radiobutton(self, text='Male', variable=gender, value='M')
		genderM.grid(row=8, column=1, sticky="w")
		genderF = tk.Radiobutton(self, text='Female', variable=gender, value='F')
		genderF.grid(row=8, column=1, sticky="w",padx = 65, pady = 5)	
		childFrame = tk.Frame(self,relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
		childFrame.grid(row = 9, column = 1)
		registerButton = ttk.Button(childFrame, text ="Register", 
		command = lambda: self.register(tuple([name.get(),password.get(),fname.get(),lname.get(),
												age.get(),city.get(),gender.get(),address.get()]),controller)) 
		registerButton.grid(row = 0, column = 0, padx = 5, pady = 5)  
		loginButton = ttk.Button(childFrame, text ="Login", 
		command = lambda : controller.frames["LoginForm"].tkraise()) 
		loginButton.grid(row = 0, column = 1, padx = 5, pady = 5) 
	
	#Validate and register new user
	def register(self,params,controller):
		flag = [not(i and i.strip()) for i in params]
		if True in flag:
			messagebox.showinfo("Registration Failed", "All the fields are required!")
			controller.frames["RegistrationForm"].tkraise()
		elif not params[4].isdigit() or int(params[4])<=0 or int(params[4])>150:
			messagebox.showinfo("Registration Failed", "Invalid age!")
			controller.frames["RegistrationForm"].tkraise()
		else:
			sql = "SELECT EXISTS(SELECT * FROM users WHERE username=?)"
			rows = get_records(sql,tuple([params[0]]))
			if rows[0][0]:
				messagebox.showinfo("Registration Failed", "Username already exists!")
				controller.frames["RegistrationForm"].tkraise()
			else:
				sql = """INSERT OR IGNORE INTO users(userid,username,password,firstname,lastname,age,city,gender,address) VALUES((SELECT IFNULL(MAX(userid), 0)+1 FROM users),?,?,?,?,?,?,?,?)"""
				res = insert_record(sql,params)
				if res:
					messagebox.showinfo("Registration Done", "Registration successfull!")				
					self.username = params[0]
					sql = "SELECT userid FROM users WHERE username=?"
					res = get_records(sql,tuple([params[0]]))
					self.userid = res[0][0]
					controller.frames["AppointmentForm"].tkraise_reg()
				else:
					messagebox.showinfo("Registration Failed", "Contact Admin!")
					controller.frames["RegistrationForm"].tkraise()

# third window frame AppointmentForm 
class AppointmentForm(tk.Frame): 
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 
		self.login = controller.frames["LoginForm"]
		self.register = controller.frames["RegistrationForm"]
		textLabel = tk.Label(self, text="Appointment Form")
		textLabel.grid(row=0, column=1,padx = 40, pady = 10)
		idLabel = tk.Label(self, text="UserId:")
		idLabel.grid(row=1, column=0,padx = 5, pady = 5)
		self.idText = tk.StringVar()
		id = tk.Entry(self,textvariable=self.idText, width=30,state='readonly')
		id.grid(row=1, column=1,padx = 5, pady = 5)
		nameLabel = tk.Label(self, text="Username:")
		nameLabel.grid(row=2, column=0,padx = 5, pady = 5)
		self.nameText = tk.StringVar()
		name = tk.Entry(self, textvariable=self.nameText, width=30,state='readonly')
		name.grid(row=2, column=1,padx = 5, pady = 5)
		dateLabel = tk.Label(self, text="Appointment Date:")
		dateLabel.grid(row=3, column=0,padx = 5, pady = 5)
		date = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
		
		date.grid(row=3, column=1,padx = 5, pady = 5)
		timeLabel = tk.Label(self, text="Appointment Time:")
		timeLabel.grid(row=4, column=0,padx = 5, pady = 5)
		time = tk.StringVar(self)
		choices = ['10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45','12:00','12:15',\
				   '12:30','12:45','1:00','1:15','1:30','1:45','2:00','2:15','2:30','2:45']
		time.set('10:00')
		timepopupMenu = tk.OptionMenu(self, time, *choices)
		timepopupMenu.grid(row=4,column=1,padx = 5, pady = 5)
		doctorLabel = tk.Label(self, text="Doctor:")
		doctorLabel.grid(row=5, column=0,padx = 5, pady = 5)
		doctor = tk.StringVar(self)
		choices_ = ['Andy','Charlie']
		doctor.set('Andy')
		doctorpopupMenu = tk.OptionMenu(self, doctor, *choices_)
		doctorpopupMenu.grid(row = 5, column = 1,padx = 5, pady = 5)
		childFrame = tk.Frame(self,relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
		childFrame.grid(row = 6, column = 1,padx = 5, pady = 5)
		checkAvailablityButton = ttk.Button(childFrame, text ="Check Availability", 
		command = lambda: self.checkAvail(tuple([id.get(),name.get(),date.get_date(),time.get(),doctor.get()]),controller)) 
		checkAvailablityButton.grid(row = 0, column = 0, padx = 5, pady = 5)  
		bookedButton = ttk.Button(childFrame, text ="Appointments booked", 
		command = lambda : controller.frames["BookedForm"].tkraise()) 
		bookedButton.grid(row = 0, column = 1, padx = 5, pady = 5) 
		logoutButton = ttk.Button(childFrame, text ="Logout", 
		command = lambda : controller.frames["LoginForm"].tkraise()) 
		logoutButton.grid(row = 0, column = 2, padx = 5, pady = 5) 
	
	#Get value for user login
	def tkraise_(self):
		self.username = self.login.username
		self.userid = self.login.userid
		self.idText.set(self.userid)
		self.nameText.set(self.username)
		tk.Frame.tkraise(self)

	#Get value for new user registered
	def tkraise_reg(self):
		self.username = self.register.username
		self.userid = self.register.userid
		self.idText.set(self.userid)
		self.nameText.set(self.username)
		tk.Frame.tkraise(self)

	#Check availability and book appointment
	def checkAvail(self,params,controller):
		today = datetime.date.today()
		if today>=params[2]:
			messagebox.showinfo("Booking Failed", "Select a valid date!")
			controller.frames["AppointmentForm"].tkraise()
		else:
			sql = "SELECT userid,doctorName FROM availability WHERE appointmentDate=? AND appointmentTime=?"
			rows = get_records(sql,tuple([params[2],params[3]]))
			flag = False
			if len(rows)>0:
				for row in rows:
					if str(row[0])==str(params[0]):
						flag = True
						messagebox.showinfo("Booking Failed", "You already have scheduled appointment at this slot!")
						controller.frames["AppointmentForm"].tkraise()
					elif row[1]==params[4]:
						flag = True
						messagebox.showinfo("Booking Failed", "Slot not available!")
						controller.frames["AppointmentForm"].tkraise()
			if not flag:
				sql = """INSERT OR IGNORE INTO availability(userid,username,appointmentDate,appointmentTime,doctorName) VALUES(?,?,?,?,?)"""
				res = insert_record(sql,params)
				if res:
					messagebox.showinfo("Booking Done", "Booking confirmed!")
					controller.frames["AppointmentForm"].tkraise()
				else:
					messagebox.showinfo("Registration Failed", "Contact Admin!")
					controller.frames["AppointmentForm"].tkraise()



# fourth window frame bookedForm 
class BookedForm(tk.Frame): 
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent) 
		self.controller = controller
		self.parent = parent
		textLabel = tk.Label(self, text="Appointments Booked")
		textLabel.grid(row=0, column=0,padx = 40, pady = 10)
		logoutButton = ttk.Button(self, text ="Back", 
		command = lambda : controller.frames["AppointmentForm"].tkraise()) 
		logoutButton.grid(row = 0, column = 1, padx = 5, pady = 5) 
	
	#Populate appointments data
	def tkraise(self):
		childFrame = tk.Frame(self,relief=tk.RAISED, borderwidth=1, padx=2, pady=2)
		childFrame.grid(row = 1, column = 0,padx = 5, pady = 5)
		sql = "SELECT * FROM availability ORDER BY userid,appointmentDate,appointmentTime"
		e1 = tk.Entry(childFrame,width=10,font=('Arial',10,'bold'))
		e1.grid(row=0, column=0)
		e1.insert(0, "UserId")
		e1.configure(state='readonly')
		e2 = tk.Entry(childFrame, width=10,font=('Arial',10,'bold'))
		e2.grid(row=0, column=1)
		e2.insert(0, "UserName")
		e2.configure(state='readonly')
		e3 = tk.Entry(childFrame,width=10,font=('Arial',10,'bold'))
		e3.grid(row=0, column=2)
		e3.insert(0, "AppDate")
		e3.configure(state='readonly')
		e4 = tk.Entry(childFrame,width=10,font=('Arial',10,'bold'))
		e4.grid(row=0, column=3)
		e4.insert(0, "AppTime")
		e4.configure(state='readonly')
		e5 = tk.Entry(childFrame,width=10,font=('Arial',10,'bold'))
		e5.grid(row=0, column=4)
		e5.insert(0, "Doctor")
		e5.configure(state='readonly')
		rows = get_all_records(sql)
		for i in range(len(rows)): 
			for j in range(5):
				self.e = tk.Entry(childFrame, fg='blue',width=10,font=('Arial',10,'bold'))
				self.e.grid(row=i+1, column=j)
				self.e.insert(0, rows[i][j])
				self.e.configure(state='readonly') 
		tk.Frame.tkraise(self)