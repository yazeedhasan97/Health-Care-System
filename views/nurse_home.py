import re
import tkinter as tk
from tkinter import ttk
from models.db import DBConnection as db
from utility.constants import LIST_OF_ALLERGIES
from views.home import Home
from views.login import LoginScreen
from tkinter import messagebox as mb


class NurseHome(Home):
    def __init__(self, employee):
        super().__init__(employee)

    def init_left_components(self):
        self.btn_add_patient = tk.Button(self.frm_left, text='Add Patient', width=30,
                                         command=lambda x=1: self.show_right_components(x))

        self.btn_initial_assessment = tk.Button(self.frm_left, text='Patient Initial Assessment', width=30,
                                                command=lambda x=2: self.show_right_components(x))

        self.btn_add_patient.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.btn_initial_assessment.grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=5)

    def init_right_frames(self):
        self.frm_add_patient = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#00F84F')
        self.init_frm_add_patient()

        self.frm_initial_assessment = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#FFFF00')
        self.init_frm_initial_assessment()

    def show_right_components(self, state=0):
        if state == 0:
            self.frm_personal_info.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_add_patient.pack_forget()
            self.frm_initial_assessment.pack_forget()
        elif state == 1:
            self.frm_add_patient.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_initial_assessment.pack_forget()
        elif state == 2:
            self.frm_initial_assessment.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_add_patient.pack_forget()

    def init_frm_add_patient(self):
        ## ADD ##

        # labels and first 4 entries
        labels = ('ID', 'name', 'phone', 'address', 'gender', 'age', 'allergies')
        add_results = [None] * len(labels)
        pos = 0
        for text in labels[:-1]:
            tk.Label(self.frm_add_patient, text='Patient ' + text, anchor='w', width=20, relief='groove') \
                .place(relx=.05, rely=.1 + pos / 16, height=40, width=170)

            if pos < 4:
                add_results[pos] = tk.Entry(self.frm_add_patient, width=25)
                add_results[pos].place(relx=.25, rely=.1 + pos / 16, height=35, width=200)
            pos += 1

        # gender
        frm_radio_buttons = tk.Frame(self.frm_add_patient)
        frm_radio_buttons.place(relx=.25, rely=.1 + 4 / 16, height=40, width=200)
        add_results[4] = tk.StringVar()
        add_results[4].set('Male')
        tk.Radiobutton(frm_radio_buttons, text="Male", variable=add_results[4], value='male') \
            .pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)
        tk.Radiobutton(frm_radio_buttons, text="Female", variable=add_results[4], value='female') \
            .pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)

        # age
        add_results[5] = tk.Scale(self.frm_add_patient, from_=0, to=115, length=115, sliderrelief='flat',
                                  orient=tk.HORIZONTAL, highlightthickness=0, background='black',
                                  fg='grey', troughcolor='#73B5FA', activebackground='#1065BF')
        add_results[5].set(27)
        add_results[5].place(relx=.25, rely=.1 + 5 / 16, anchor='nw', width=200, height=40)

        tk.Label(self.frm_add_patient, text='Do the patient has any allergies ?', anchor='c', width=20, relief='groove',
                 font=("Courier", 14)) \
            .place(relx=.5, rely=.1 + 0 / 16, height=35, width=400)

        allergi = ttk.Combobox(self.frm_add_patient, state="readonly",
                               values=["Select ALLERGIC"] + LIST_OF_ALLERGIES)
        allergi.set('Select ALLERGIC')
        allergi.place(relx=.5, rely=.1 + 1 / 16, anchor='nw', height=30, width=200)

        add_results[6] = tk.Text(self.frm_add_patient)
        add_results[6].place(relx=.5, rely=.1 + 2 / 16, anchor='nw', height=120, width=280)

        ttk.Button(self.frm_add_patient, text='Add', command=lambda: self.add_alergi(allergi, add_results[6])) \
            .place(relx=.75, rely=.1 + 1 / 16, anchor='nw', width=80, height=30)

        ttk.Button(self.frm_add_patient, text='Add Patient', command=lambda: self.addPatient(add_results)) \
            .place(relx=.6, rely=.1 + 5 / 16, anchor='nw', width=180, height=40)

        # image
        # from tkinter import ttk
        # ttk.Button(self.frm_add_patient, width=25, text='chose image', command=lambda: self.select_image(add_results)) \
        #     .place(relx=.4, rely=.1 + 7 / 16, anchor='nw', width=200, height=40)

        # role
        # # tk.Label(self.frm_docs, text="User Role*").place(relx=.2, rely=.1 + 8 / 16, height=40, width=170)
        # add_results[8] = ttk.Combobox(self.frm_add_patient, state="readonly", values=["doctor", "nurse", "admin"])
        # add_results[8].set('doctor')
        # add_results[8].place(relx=.4, rely=.1 + 9 / 16, anchor='nw', width=200, height=40)
        #
        # # button
        # tk.Button(self.frm_add_patient, width=25, text='Add User', command=lambda: self.add_user(add_results)) \
        #     .place(relx=.7, rely=.1 + 8 / 16, anchor='nw', width=200, height=50)
        #
        # ## Remove ##
        # tk.Label(self.frm_add_patient, text='Remove User: ', anchor='w', width=20, font=("Helvetica", 16, "bold"),
        #          relief='groove').place(relx=.005, rely=.1 + 10 / 16, height=45, width=160)
        #
        # tk.Label(self.frm_add_patient, text="Email").place(relx=.2, rely=.1 + 11 / 16, height=40, width=180)
        # user_id = tk.Entry(self.frm_add_patient)
        # user_id.place(relx=.4, rely=.1 + 11 / 16, height=40, width=200)
        #
        # tk.Button(self.frm_add_patient, text='Remove User', command=lambda: self.remove_user(user_id.get())) \
        #     .place(relx=.7, rely=.1 + 11 / 16, anchor='nw', width=200, height=50)
        pass

    def add_alergi(self, cbox, text_area):
        if cbox.get() == 'Select ALLERGIC':
            mb.showwarning('Warning', "Please select a valid ALLERGIC.")
            return
        if text_area.compare("end-1c", "==", "1.0"):
            text_area.insert(tk.INSERT, cbox.get() + '\n')
        else:
            text_area.insert(tk.END, cbox.get() + '\n')

    def addPatient(self, add_results):
        pid = add_results[0].get()
        name = add_results[1].get()
        phone = add_results[2].get()
        address = add_results[3].get()
        gender = add_results[4].get()
        age = add_results[5].get()
        allergic = set(add_results[6].get('1.0', 'end-1c').splitlines())

        if not pid:
            mb.showwarning('Required Field', "'ID' is required!")
            return

        if not re.match(r'[0-9]+', pid):
            mb.showwarning('Required Field', "'ID' must be all numbers!")
            return

        results = tuple(db().getConn().execute(
            f"select * from private.patiant "
            f"where id = {pid};"))

        res = 'NO'
        if results:
            res = mb.askyesnocancel('Found',
                                    f'a patient with id {pid} is registered in the system under the name "{results[0][1]}";\n'
                                    f' do you want to continue and overwrite his data?')

            if not res:
                return

        if phone and (not re.match(r'[0-9]+', phone) or len(phone) < 10):
            mb.showwarning('Validity Error', "Please enter a valid phone number!")
            return

        if not name:
            mb.showwarning('Required Field', "'Name' is required!")
            return
        print(res)
        if not results:
            db().getConn().execute(
                f"insert into private.patiant (id, name, age, gender , phone , address) "
                f"values ({pid}, '{name}', '{age}', '{gender}', '{phone}', '{address}');")

        elif results and res:
            db().getConn().execute(
                f"UPDATE private.patiant SET "
                f"name = '{name}', "
                f"age = '{age}', "
                f"gender = '{gender}', "
                f"address = '{address}', "
                f"phone = '{phone}' "
                f"where id = {pid};")

        db().getConn().execute(
            f"DELETE from private.allergies "
            f"where p_id = {pid};")

        for item in allergic:
            db().getConn().execute(
                f"insert into private.allergies (p_id, allergie) "
                f"values ({pid}, '{item}');")
        mb.showinfo('Required Field', "Patient Added successfully")
        pass

    def init_frm_initial_assessment(self):

        labels = ('ID', 'Heart Rate', 'Tempreture')
        add_results = [None] * (len(labels) + 1)

        for idx, text in enumerate(labels, start=1):
            tk.Label(self.frm_initial_assessment, text='Patient ' + text, anchor='w', width=20, relief='groove') \
                .place(relx=.05, rely=.1 + idx / 16, height=40, width=170)

        add_results[0] = tk.Entry(self.frm_initial_assessment, width=25)
        add_results[0].place(relx=.25, rely=.1 + 1 / 16, height=35, width=200)

        add_results[1] = tk.Scale(self.frm_initial_assessment, from_=40, to=120, length=120 - 40, sliderrelief='flat',
                                  orient=tk.HORIZONTAL, highlightthickness=0, background='black',
                                  fg='grey', troughcolor='#73B5FA', activebackground='#1065BF')
        add_results[1].set(60)
        add_results[1].place(relx=.25, rely=.1 + 2 / 16, anchor='nw', width=200, height=40)

        add_results[2] = tk.Scale(self.frm_initial_assessment, from_=34, to=40, length=7, sliderrelief='flat',
                                  orient=tk.HORIZONTAL, highlightthickness=0, background='black',
                                  fg='grey', troughcolor='#73B5FA', activebackground='#1065BF')
        add_results[2].set(37)
        add_results[2].place(relx=.25, rely=.1 + 3 / 16, anchor='nw', width=200, height=40)

        from datetime import datetime as dt
        add_results[3] = dt.now()

        ttk.Button(self.frm_initial_assessment, text='Add', command=lambda: self.addInitialAssessment(add_results)) \
            .place(relx=.5, rely=.1 + 2.5 / 16, anchor='nw', width=180, height=40)

        pass

    def addInitialAssessment(self, add_results):
        pid = add_results[0].get()
        if not pid:
            mb.showwarning('Required Field', "'ID' is required!")
            return

        if not re.match(r'[0-9]+', pid):
            mb.showwarning('Required Field', "'ID' must be all numbers!")
            return

        results = tuple(db().getConn().execute(
            f"select * from private.patiant "
            f"where id = {pid};"))

        if not results:
            mb.showinfo('Not Found', f'Patiant with ID {pid} is not registered in the system')
            return

        db().getConn().execute(
            f"insert into private.user_to_pat (p_id, arrival_time, heart_rate, tempreture) "
            f"values ({pid}, '{add_results[3]}', '{add_results[1].get()}', '{add_results[2].get()}');")

        mb.showinfo('Required Field', "Data Added successfully")
        pass

