from views.home import Home
from views.login import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sd
from tkinter import filedialog as fd
from models.db import DBConnection as db
import functools as ft
import operator
from tkcalendar import DateEntry


class ManagerHome(Home):
    def __init__(self, employee):
        self.img_path = ''
        super().__init__(employee)

    def init_left_components(self):
        self.btn_add_doc = tk.Button(self.frm_left, text='Users', width=30,
                                     command=lambda x=1: self.show_right_components(x))

        self.btn_doc_report = tk.Button(self.frm_left, text='Doctors Report', width=30,
                                        command=lambda x=3: self.show_right_components(x))

        self.btn_patient_report = tk.Button(self.frm_left, text='Patients Report', width=30,
                                            command=lambda x=4: self.show_right_components(x))

        self.btn_add_doc.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.btn_doc_report.grid(row=5, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.btn_patient_report.grid(row=6, column=0, padx=5, pady=5, ipadx=5, ipady=5)

    def init_right_frames(self):
        self.frm_docs = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#00FFFF')
        self.init_frm_docs()

        self.frm_doc_report = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#F91F00')
        self.init_frm_doc_report()

        self.frm_patient_report = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#52FF00')
        self.init_frm_patient_report()

    def show_right_components(self, state=0):
        if state == 0:
            self.frm_personal_info.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_docs.pack_forget()
            self.frm_doc_report.pack_forget()
            self.frm_patient_report.pack_forget()
        elif state == 1:
            self.frm_docs.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_doc_report.pack_forget()
            self.frm_patient_report.pack_forget()
        elif state == 2:
            self.frm_docs.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_doc_report.pack_forget()
            self.frm_patient_report.pack_forget()
        elif state == 3:
            self.frm_doc_report.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_docs.pack_forget()
            self.frm_patient_report.pack_forget()
        elif state == 4:
            self.frm_patient_report.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_docs.pack_forget()
            self.frm_doc_report.pack_forget()

    def init_frm_docs(self):

        ## ADD ##
        tk.Label(self.frm_docs, text='Create User: ', anchor='w', width=20, font=("Helvetica", 16, "bold"),
                 relief='groove').place(relx=.005, rely=.005, height=45, width=140)

        # labels and first 4 entries
        labels = ('email', 'name*', 'initial password*', 'phone', 'address', 'gender', 'age', 'image', 'role*')
        add_results = [None] * len(labels)
        pos = 0
        for text in labels:
            if 'role' in text:
                pos += 1
            tk.Label(self.frm_docs, text='User ' + text, anchor='w', width=20, relief='groove') \
                .place(relx=.2, rely=.1 + pos / 16, height=40, width=170)

            if pos < 5:
                add_results[pos] = tk.Entry(self.frm_docs, width=25)
                add_results[pos].place(relx=.4, rely=.1 + pos / 16, height=35, width=200)
            pos += 1

        # gender
        frm_radio_buttons = tk.Frame(self.frm_docs)
        frm_radio_buttons.place(relx=.4, rely=.1 + 5 / 16, height=40, width=200)
        add_results[5] = tk.StringVar()
        add_results[5].set('M')
        tk.Radiobutton(frm_radio_buttons, text="Male", variable=add_results[4], value='M') \
            .pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)
        tk.Radiobutton(frm_radio_buttons, text="Female", variable=add_results[4], value='F') \
            .pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)

        # age
        add_results[6] = tk.Scale(self.frm_docs, from_=22, to=65, length=65, sliderrelief='flat',
                                  orient=tk.HORIZONTAL, highlightthickness=0, background='black',
                                  fg='grey', troughcolor='#73B5FA', activebackground='#1065BF')
        add_results[6].set(30)
        add_results[6].place(relx=.4, rely=.1 + 6 / 16, anchor='nw', width=200, height=40)

        # image
        tk.Button(self.frm_docs, width=25, text='chose image', command=lambda: self.select_image(add_results)) \
            .place(relx=.4, rely=.1 + 7 / 16, anchor='nw', width=200, height=40)

        # role
        # tk.Label(self.frm_docs, text="User Role*").place(relx=.2, rely=.1 + 8 / 16, height=40, width=170)
        add_results[8] = ttk.Combobox(self.frm_docs, state="readonly", values=["admin", "doctor", "nurse"])
        add_results[8].set('doctor')
        add_results[8].place(relx=.4, rely=.1 + 9 / 16, anchor='nw', width=200, height=40)

        # button
        tk.Button(self.frm_docs, width=25, text='Add User', command=lambda: self.add_user(add_results)) \
            .place(relx=.7, rely=.1 + 8 / 16, anchor='nw', width=200, height=50)

        ## Remove ##
        tk.Label(self.frm_docs, text='Remove User: ', anchor='w', width=20, font=("Helvetica", 16, "bold"),
                 relief='groove').place(relx=.005, rely=.1 + 10 / 16, height=45, width=160)

        tk.Label(self.frm_docs, text="Email").place(relx=.2, rely=.1 + 11 / 16, height=40, width=180)
        user_id = tk.Entry(self.frm_docs)
        user_id.place(relx=.4, rely=.1 + 11 / 16, height=40, width=200)

        tk.Button(self.frm_docs, text='Remove User', command=lambda: self.remove_user(user_id.get())) \
            .place(relx=.7, rely=.1 + 11 / 16, anchor='nw', width=200, height=50)

        pass

    def select_image(self, lst):
        ftypes = [
            ('PNG images', '*.png'),
            ('JPEG, JPG images', '*.jpeg;*.jpg'),  # semicolon trick
            ('All files', '*'),
        ]
        lst[7] = fd.askopenfilename(filetypes=ftypes)
        tk.Label(self.frm_docs, width=25, text=lst[7][lst[7].rfind('/') + 1:]) \
            .place(relx=.4, rely=.1 + 8 / 16, anchor='nw', width=200, height=40)

    def add_user(self, lstData):
        email = lstData[0].get()
        name = lstData[1].get()
        password = lstData[2].get()
        phone = lstData[3].get()
        address = lstData[4].get()
        gender = lstData[5].get()
        age = lstData[6].get()
        image = lstData[7] if lstData[7] is not None and lstData[7] != '' else '../static/person.jpg'
        role = lstData[8].current()

        if not email:
            mb.showwarning('Warning', 'Email is required.')
            return
        if not re.fullmatch(r'.+@.+\.com', email):
            mb.showwarning('Warning', 'Email must be in email format (eg. myemail@demail.com).')
            return

        if not name:
            mb.showwarning('Warning', "'Name' is required")
            return
        if not password:
            mb.showwarning('Warning', "'Password' is required")
            return
        if phone and not re.fullmatch(r'[0-9]+', phone):
            mb.showwarning('Warning', "'Phone' must be all numbers.")
            return

        # answer = sd.askstring("Doctor major", f"What is {name} major?", parent=self.frm_docs)
        # if answer is None and answer == '':
        #     mb.showwarning("'Major' is required")
        #     return

        db().getConn().execute(
            f"insert into private.users (email, name, password, age, role, gender, phone, address, image)"
            f" values ('{email}', '{name}', '{password}', {age}, {role}, '{gender}', '{phone}', '{address}', '{image}');")

        mb.showinfo('Warning', "User Added successfully")

    def remove_user(self, email):
        if not email:
            mb.showwarning('Warning', "Please enter an email.")
            return

        if not re.fullmatch(r'.+@.+\.com', email):
            mb.showwarning('Warning', 'Email must be in email format (eg. myemail@demail.com).')
            return

        db().getConn().execute(f"DELETE FROM private.users "
                               f" WHERE  email = '{email}';")
        mb.showinfo('Warning', "User removed successfully")
        pass

    def init_frm_doc_report(self):

        doctors_list = list(db().getConn().execute("Select email from private.users where role = 1;"))
        doctors_list = ft.reduce(operator.iconcat, doctors_list, [])

        doctor = ttk.Combobox(self.frm_doc_report, state="readonly",
                              values=["Select Doctor"] + doctors_list)
        doctor.set('Select Doctor')
        doctor.place(relx=.075, rely=.1 + 11.5 / 16, anchor='nw', height=30, width=200)

        tk.Label(self.frm_doc_report, text='Start Date', anchor='w', width=10, relief='groove') \
            .place(relx=.325, rely=.1 + 11.5 / 16, height=30)

        start_date = DateEntry(self.frm_doc_report, width=15, background='darkblue', year=2019, month=6, day=17,
                               foreground='white', borderwidth=2, state='readonly')
        start_date.place(relx=.415, rely=.1 + 11.5 / 16, height=30)

        tk.Label(self.frm_doc_report, text='End Date', anchor='w', width=10, relief='groove') \
            .place(relx=.325, rely=.1 + 12.5 / 16, height=30)

        end_date = DateEntry(self.frm_doc_report, width=15, background='darkblue',
                             foreground='white', borderwidth=2, state='readonly')
        end_date.place(relx=.415, rely=.1 + 12.5 / 16, height=30)

        cols = ('Email', 'Name', 'Number of Visits', 'Date')
        listBox = ttk.Treeview(self.frm_doc_report, columns=cols, show='headings', selectmode='browse')

        # set column headings
        for col in cols:
            listBox.heading(col, text=col)
            listBox.column(col, minwidth=100, width=205, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(self.frm_doc_report, orient="vertical", command=listBox.yview)
        vsb.place(relx=.925, rely=.05, height=500)

        listBox.configure(yscrollcommand=vsb.set)

        listBox.place(relx=.05, rely=.05, height=500, width=820)

        tk.Button(self.frm_doc_report, text='Generate',
                  command=lambda: self.generate_doc_report(doctor.get(), start_date.get_date(), end_date.get_date(),
                                                           listBox)) \
            .place(relx=.6, rely=.1 + 11.3 / 16, anchor='nw', width=180, height=40)

        tk.Button(self.frm_doc_report, text='Clear', command=lambda: self.clear_table(listBox)) \
            .place(relx=.6, rely=.1 + 12.3 / 16, anchor='nw', width=180, height=40)

    def clear_table(self, listBox):
        listBox.delete(*listBox.get_children())

    def generate_doc_report(self, doctor, start_date, end_date, listBox):
        if doctor == "Select Doctor":
            mb.showwarning('Warning', "Please select a valid doctor.")
            return

        if start_date > end_date:
            mb.showwarning('Warning', "'Start Date' must be before or same as 'End Date'")
            return

        result = db().getConn().execute(f"select max(u.email), max(u.name), max(u.id), count(s.p_id), s.s_date "
                                        f"from private.users as u "
                                        f"Inner Join private.session as s "
                                        f"on u.id = s.u_id "
                                        f"where s.s_date between '{start_date}' and '{end_date}' "
                                        f"group by s.s_date order by s.s_date;")

        result = tuple(result)
        if not result:
            mb.showwarning('Warning', f"No data found for {doctor} in the specified dates.")
            return

        for item in result:
            listBox.insert("", "end", values=(item[0], item[1], item[3], item[4]))
            pass

    def init_frm_patient_report(self):
        from tkcalendar import DateEntry

        tk.Label(self.frm_patient_report, text='Date', anchor='w', width=10, relief='groove') \
            .place(relx=.075, rely=.1, height=30)

        date = DateEntry(self.frm_patient_report, width=16, background='darkblue', year=2020, month=1, day=2,
                         foreground='white', borderwidth=2, state='readonly')
        date.place(relx=.160, rely=.1, height=30)

        tk.Label(self.frm_patient_report, text='Patients Average Waiting Time:', anchor='w', width=25, relief='groove') \
            .place(relx=.075, rely=.1 + 8 / 16, height=40)

        avg_result = tk.Label(self.frm_patient_report, text=f'', anchor='w', width=25, relief='groove')
        avg_result.place(relx=.075, rely=.1 + 9 / 16, height=30)

        cols = ('ID', 'Name', 'Arrival Time', 'Start Time', 'Waiting Time')
        listBox = ttk.Treeview(self.frm_patient_report, columns=cols, show='headings', selectmode='browse')
        # set column headings
        for col in cols[:3]:
            listBox.heading(col, text=col)
            listBox.column(col, minwidth=50, width=70)
        for col in cols[3:]:
            listBox.heading(col, text=col)
            listBox.column(col, minwidth=50, width=145)

        vsb = ttk.Scrollbar(self.frm_patient_report, orient="vertical", command=listBox.yview)
        vsb.place(relx=.945, rely=.05, height=550)
        listBox.configure(yscrollcommand=vsb.set)

        listBox.place(relx=.32, rely=.05, height=550, width=590)

        tk.Button(self.frm_patient_report, text='Show',
                  command=lambda: self.showWaitingTimes(listBox, avg_result, date.get_date())) \
            .place(relx=.075, rely=.1 + 1 / 16, anchor='nw', width=200, height=40)

        tk.Button(self.frm_patient_report, text='Clear',
                  command=lambda: self.clear_table(listBox)) \
            .place(relx=.075, rely=.1 + 2 / 16, anchor='nw', width=200, height=40)

    def showWaitingTimes(self, listBox, avg_result, date):
        result = db().getConn().execute(
            f"select up.p_id, p.name , up.arrival_time, s.start_time, (s.start_time - up.arrival_time) as wait_time  "
            f"from private.user_to_pat as up "
            f"inner join private.session as s "
            f"on up.p_id = s.p_id and date(up.arrival_time) = date(s.start_time) "
            f"inner join private.patiant as p "
            f"on p.id = up.p_id "
            f"where date(up.arrival_time) = '{date}';")

        result = tuple(result)

        if not result:
            mb.showwarning('Warning', f"No data found for the specified dates.")
            return

        avg_time = result[0][4]
        for item in result:
            avg_time += item[4]
            listBox.insert("", "end", values=(item[0], item[1], item[2].time(), item[3].time(), item[4]))
        avg_time -= result[0][4]
        avg_result["text"] = str(avg_time)

