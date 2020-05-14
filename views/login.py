import os
import pickle

import re

import tkinter as tk
import tkinter.messagebox as mb

from models.db import DBConnection as db
from models.employees import Employee

from utility.utility import centerWindow, random_alphaNumeric_password

TEMP_PASS = False


class LoginScreen:
    def __init__(self):
        self.window = tk.Tk(className='Login')
        self.window.minsize(400, 150)
        self.window.maxsize(400, 150)
        centerWindow(self.window)
        self.init_component()
        if os.path.exists('../static/files/user.pkl'):
            user = self.getMe()
            if not (user is None or user.email == ''):
                self.nextScreen(user.role, user)

        self.window.mainloop()

    def init_component(self):
        self.frm_input = tk.Frame(self.window, width=300, height=100)  # , background="#9C0863"
        self.lbl_name = tk.Label(self.frm_input, text='Email')
        self.lbl_pass = tk.Label(self.frm_input, text='Password')

        self.lbl_name.grid(row=0, column=0, sticky=tk.W, ipady=4)
        self.lbl_pass.grid(row=1, column=0, sticky=tk.W, ipady=4)

        self.ent_email = tk.Entry(self.frm_input, width=50)
        self.ent_pass = tk.Entry(self.frm_input, width=50, show="*")

        self.ent_email.grid(row=0, column=1, padx=3, pady=7)
        self.ent_pass.grid(row=1, column=1, padx=3, pady=7)

        self.frm_input.pack(padx=5, pady=10)

        self.frm_buttons = tk.Frame(self.window, width=300, height=100)

        self.btn_login = tk.Button(self.frm_buttons, text='Login', width=15, height=2, command=self.checkForUser)
        self.btn_empty = tk.Button(self.frm_buttons, text='Forget Password', width=15, height=2,
                                   command=self.forgetPassword)
        self.btn_empty.pack(side=tk.RIGHT, padx=4, pady=2)
        self.btn_login.pack(side=tk.RIGHT, padx=4, pady=2)
        self.frm_buttons.pack(side=tk.RIGHT, padx=5, pady=10)
        pass

    def checkForUser(self):
        email = self.ent_email.get()
        password = self.ent_pass.get()
        if email == '' or password == '':
            mb.showwarning('Warning', 'All Fields are required.')
            return
        if not re.fullmatch(r'.+@.+\.com', email):
            mb.showwarning('Warning', 'Email must be in email format (eg. myemail@demail.com).')
            return

        result = tuple(db().getConn().execute(f'select email, name, password, role, image from private.users where '
                                              f"email = '{email}';"))

        if not result:
            mb.showwarning('Error', f'User with email: {email} not registered in the system')
            return

        if result[0][2] != password:
            mb.showwarning('Error', f'Password is incorrect')
            return

        print(result[0][0])

        user = Employee(email=result[0][0], name=result[0][1], password=result[0][2], role=result[0][3],
                        image=result[0][4])

        self.rememberMe(user)
        self.nextScreen(role=result[0][3], user=user)

    def forgetPassword(self):
        from email.message import EmailMessage
        import smtplib
        import datetime as dt
        reciver_email = self.ent_email.get()

        EMAIL = ""
        PASSWORD = ''
        if reciver_email == '':
            mb.showwarning('Warning', 'Email is required.')
            return

        results = tuple(db().getConn().execute(f'select email from private.users where '
                                               f"email = '{reciver_email}';"))

        if results[0] is None or results[0][0] == '':
            mb.showwarning('Warning', 'This user is not registered in the system')
            return

        new_password = random_alphaNumeric_password(6, 4)

        msg = EmailMessage()
        msg["Subject"] = f"Password Recovery Email | HCS | {dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
        msg["From"] = EMAIL
        msg["To"] = [reciver_email]
        msg.set_content(f'Please use this password as temporary password to enter the system: '
                        f' {new_password}')
        # msg.add_attachment(f'Please use this password as temporary password to enter the system:'
        #                    f'{new_password}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        db().getConn().execute(
            f"UPDATE private.users SET "
            f"password = '{new_password}' "
            f"where email = '{reciver_email}';")

        mb.showwarning('Info', 'An email with temporary password is sent to you email.')
        global TEMP_PASS
        TEMP_PASS = True

    def nextScreen(self, role, user):
        self.window.destroy()
        if role == 0:
            from views.maneger_home import ManagerHome
            ManagerHome(user)
        elif role == 1:
            from views.doctor_home import DoctorHome
            DoctorHome(user)
        elif role == 2:
            from views.nurse_home import NurseHome
            NurseHome(user)

    def rememberMe(self, user):
        with open('../static/files/user.pkl', 'bw') as file:
            pickle.dump(user, file)

    def getMe(self):
        with open('../static/files/user.pkl', 'rb') as file:
            user = pickle.load(file)
        return user
