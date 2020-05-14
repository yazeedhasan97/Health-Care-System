import os
import tkinter as tk
import tkinter.messagebox as mb
from abc import ABC, abstractmethod

from PIL import ImageTk, Image
from utility.utility import centerWindow
import views.login as lg
from models.db import DBConnection as db


class Home(ABC):
    """Not meant to be instantiate. """

    def __init__(self, employee):
        self.employee = employee
        self.window = tk.Tk(className='Home Page')
        self.window.minsize(1200, 700)
        self.window.maxsize(1200, 700)
        centerWindow(self.window)
        self.init_main_frames()
        self.init_left_components()
        self.init_right_frames()

        if lg.TEMP_PASS:
            self.changeTempPass()

        self.window.mainloop()

    def init_main_frames(self):
        self.frm_left = tk.Frame(self.window, bg='#745886', relief='raised', borderwidth=5)
        self.frm_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, ipadx=5, ipady=5)

        self.lbl_name = tk.Label(self.frm_left, relief='groove',
                                 text=f"WELCOME {'Doc. ' if self.employee.role == 1 else 'Nur. ' if self.employee.role == 2 else 'Mr. '} {self.employee.name.capitalize()}",
                                 width=29, bg='#1896C0')

        image = Image.open(self.employee.image).resize((200, 250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image, master=self.frm_left)
        self.lbl_image = tk.Label(self.frm_left, image=photo, width=200, height=250)
        self.lbl_image.image = photo

        self.btn_personal_info = tk.Button(self.frm_left, text='Personal Info', width=30,
                                           command=lambda x=0: self.show_right_components(x))

        self.btn_logout = tk.Button(self.frm_left, text='Logout', width=30,
                                    command=self.logout)

        self.lbl_image.grid(row=0, column=0, padx=5, ipadx=5, ipady=5)
        self.lbl_name.grid(row=1, column=0, padx=5, ipadx=3, ipady=5, pady=1)
        self.btn_personal_info.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.btn_logout.grid(row=10, column=0, padx=5, pady=5, ipadx=5, ipady=5)

        self.init_personal_info_frame()

    def init_personal_info_frame(self):
        self.frm_personal_info = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#FF5600')
        self.frm_personal_info.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)

        pos = 4
        lables = ('Email', 'Name', 'Role', 'ID')
        values = (self.employee.email, self.employee.name.capitalize(),
                  'Doctor' if self.employee.role == 1 else 'Nurse' if self.employee.role == 2 else 'Admin',
                  self.employee.id)
        for lbl, vlu in zip(lables, values):
            tk.Label(self.frm_personal_info, relief='groove', anchor='w', text=f"{lbl}: ", width=16, height=2,
                     bg='#1896C0').place(relx=0.3, rely=pos / 15, anchor=tk.CENTER)

            tk.Label(self.frm_personal_info, relief='groove', anchor='c', text=vlu, width=25,
                     height=2, bg='#1896C0').place(relx=0.5, rely=pos / 15, anchor=tk.CENTER)

            pos += 1

        lbl2 = tk.Button(self.frm_personal_info, relief='raised', anchor='c', command=self.init_change_password,
                         borderwidth=3, text="Change Password", width=47, height=2, bg='#1896C0')
        lbl2.place(relx=0.418, rely=8 / 15, anchor=tk.CENTER)

    def logout(self):
        response = mb.askquestion("Approval", "Are you sure you want to logout ?", icon='warning')
        if response == "yes":
            self.window.destroy()
            self.forgetMe()
            del self.employee
            lg.LoginScreen()

    def init_change_password(self):
        window = tk.Tk(className='change password')
        window.minsize(350, 200)
        window.maxsize(350, 200)
        centerWindow(window)
        frm_input = tk.Frame(window)
        btn_login = tk.Button(window, text='CHANGE', width=15, height=2,
                              command=lambda x=window: self.change_pass(x))

        labels = ('Old password', 'Re-enter old password', 'New password')
        self.results = [None] * 3
        pos = 0
        for text in labels:
            tk.Label(frm_input, text=text + ':', anchor='w', width=20).grid(row=pos, column=0, sticky=tk.W,
                                                                            padx=5, pady=5, ipadx=5, ipady=5)
            self.results[pos] = tk.Entry(frm_input, text=text, width=25, show='*')
            self.results[pos].grid(row=pos, column=1, padx=5, pady=5, ipadx=5, ipady=5)
            pos += 1

        frm_input.pack(side=tk.TOP, padx=5, pady=10)
        btn_login.pack(side=tk.TOP, padx=4, pady=2)

        window.mainloop()

    def change_pass(self, window):
        old_pass = self.results[0].get()
        old_pass_con = self.results[1].get()
        new_pass = self.results[2].get()
        if not old_pass or not old_pass_con or not new_pass:
            mb.showwarning('Warning', "All fields are required !!")
            return
        if old_pass != self.employee.password:
            mb.showwarning('Warning', "Old password is incorrect !!")
            return
        if old_pass != old_pass_con:
            mb.showwarning('Warning', "The two passwords doesn't match !!")
            return
        if old_pass == new_pass:
            mb.showwarning('Warning', "The new password can't be same as old one")
            return
        approve = mb.askquestion('Change Password', 'Are you sure you want to change the password', icon='warning')
        if approve == 'yes':
            self.employee.password = new_pass
            self.employee.update()
            window.destroy()
            mb.showinfo('Success', "Password changed successfully")
            del self.results

    def changeTempPass(self):
        window = tk.Tk(className='Change Temporary Password')
        window.minsize(350, 100)
        window.maxsize(350, 100)
        centerWindow(window)

        fram = tk.Frame(window)
        fram.pack()
        tk.Label(fram, text="New Password" + ':', anchor='w', width=10) \
            .pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)
        x = tk.Entry(fram, width=25, show='*')
        x.pack(side=tk.LEFT, pady=5, ipadx=5, ipady=5)
        tk.Button(window, text="Submit", width=10, command=lambda: self.finishChangeTempPass(x, window)).pack()

        window.mainloop()

    def finishChangeTempPass(self, x, window):
        print(self.employee.email)
        db().getConn().execute(
            f"UPDATE private.users SET "
            f"password = '{x.get()}' "
            f"where email = '{self.employee.email}';")

        mb.showwarning('Info', 'Your password updated successfully.')
        window.destroy()
        pass

    def forgetMe(self):
        os.remove('../static/files/user.pkl')

    @abstractmethod
    def init_left_components(self):
        pass

    @abstractmethod
    def init_right_frames(self):
        pass

    @abstractmethod
    def show_right_components(self, state=0):
        pass
