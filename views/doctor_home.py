import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from models.db import DBConnection as db
import functools as ft
import operator
import tkinter.messagebox as mb

from tkcalendar import DateEntry
from views.home import Home
from views.login import LoginScreen


class DoctorHome(Home):
    def __init__(self, employee):
        super().__init__(employee)

    def init_left_components(self):
        self.btn_diagnose_patient = tk.Button(self.frm_left, text='Diagnose Patient', width=30,
                                              command=lambda x=1: self.show_right_components(x))

        self.btn_patiant_history = tk.Button(self.frm_left, text='Patient History', width=30,
                                             command=lambda x=2: self.show_right_components(x))

        self.btn_diagnose_patient.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.btn_patiant_history.grid(row=4, column=0, padx=5, pady=5, ipadx=5, ipady=5)

    def init_right_frames(self):
        self.frm_diag_patiant = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#00FFFF')
        self.inint_frm_diag_patiant()

        self.frm_patiant_history = tk.Frame(self.window, relief='groove', borderwidth=1, bg='#FFFF00')
        self.init_frm_patiant_history()

    def show_right_components(self, state=0):
        if state == 0:
            self.frm_personal_info.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_diag_patiant.pack_forget()
            self.frm_patiant_history.pack_forget()
        elif state == 1:
            self.frm_diag_patiant.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_patiant_history.pack_forget()
        elif state == 2:
            self.frm_patiant_history.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True)
            self.frm_personal_info.pack_forget()
            self.frm_diag_patiant.pack_forget()

    def inint_frm_diag_patiant(self):
        import datetime as dt

        tk.Label(self.frm_diag_patiant, text='Enter Patiant ID', anchor='w', width=13, relief='groove') \
            .place(relx=.02, rely=.15 / 16, height=30)

        p_id = ttk.Entry(self.frm_diag_patiant, width=9)
        p_id.place(relx=.13, rely=.15 / 16, height=30)

        cols = ('Arrival Time', 'Heart Rate', ' Temperature')
        listBox = ttk.Treeview(self.frm_diag_patiant, columns=cols, show='headings', selectmode='browse')

        ttk.Button(self.frm_diag_patiant, text='Check', command=lambda: self.add_state(listBox, p_id)) \
            .place(relx=.22, rely=.15 / 16, anchor='nw', width=90, height=30)

        ttk.Button(self.frm_diag_patiant, text='Clear', command=lambda: self.clear_table(listBox)) \
            .place(relx=.33, rely=.15 / 16, anchor='nw', width=90, height=30)

        # set column headings
        for col in cols:
            listBox.heading(col, text=col)
            listBox.column(col, minwidth=80, width=90, anchor=tk.CENTER)
        listBox.place(relx=.02, rely=1 / 16, height=80, width=270)

        start_time = dt.datetime.now()
        c_date = dt.date.today()

        tk.Label(self.frm_diag_patiant, text="Lab test requested", anchor='w', width=20, relief='groove') \
            .place(relx=.5, rely=.45 / 16, height=30)
        ent_lab_test = ttk.Entry(self.frm_diag_patiant, width=35)
        ent_lab_test.place(relx=.5, rely=1.3 / 16, height=30)

        tk.Label(self.frm_diag_patiant, text="Diagnosis", anchor='w', width=30, relief='groove') \
            .place(relx=.08 / 14, rely=3 / 16, height=30)

        diag = tk.Text(self.frm_diag_patiant, width=112, relief='groove')
        diag.place(relx=.08 / 14, rely=3.8 / 16, height=235)

        tk.Label(self.frm_diag_patiant, text="Medicine prescribed", anchor='w', width=30, relief='groove') \
            .place(relx=.08 / 14, rely=9.5 / 16, height=30)

        medic = tk.Text(self.frm_diag_patiant, width=112, relief='groove')
        medic.place(relx=.08 / 14, rely=10.3 / 16, height=235)

        ttk.Button(self.frm_diag_patiant, text='End Session',
                   command=lambda: self.end_session(start_time, c_date, ent_lab_test.get(), diag.get("1.0", tk.END),
                                                    medic.get("1.0", tk.END), p_id.get())) \
            .place(relx=.8, rely=.95 / 16, anchor='nw', width=110, height=45)



    def add_state(self, listBox, pid):
        if not pid.get():
            mb.showwarning("Error", "Patient ID is required")
            return

        results = list(db().getConn().execute(f"select arrival_time, heart_rate, tempreture "
                                              f"from private.user_to_pat "
                                              f"where p_id = {pid.get()} and n_date = date(now());"))

        if not results:
            mb.showwarning("Error", f"No Data found for patient {pid} in the system")
            return

        listBox.insert("", "end", values=(results[0][0], results[0][1], results[0][2]))
        print(results)
        pass

    def end_session(self, start_time, date, lab_test, diag, medic, pid):
        import datetime as dt
        end_time = dt.datetime.now()

        if not pid:
            mb.showwarning("Error", "Patient ID is required")
            return

        if not diag:
            mb.showwarning("Error", "You forgot to add the patient diagnostic")
            return

        if not medic:
            ans = mb.askyesno("Check", "Are you sure no medic is needed?")
            if ans == 'no':
                return

        if not lab_test:
            ans = mb.askyesno("Check", "Are you sure no lab test is needed?")
            if ans == 'no':
                return

        db().getConn().execute(
            f"insert into private.session (s_date, start_time, end_time, diag, medicine, lab_test, u_id, p_id) "
            f"values ('{date}', '{start_time}', '{end_time}', '{diag}', '{medic}', '{lab_test}', {self.employee.id}, {pid});")

        mb.showinfo("Success", "Session ended successfully")
        pass

    def init_frm_patiant_history(self):
        tk.Label(self.frm_patiant_history, text='Enter Patiant ID', anchor='w', width=13, relief='groove') \
            .place(relx=.02, rely=.15 / 16, height=30)

        p_id = ttk.Entry(self.frm_patiant_history, width=9)
        p_id.place(relx=.13, rely=.15 / 16, height=30)

        cols = 'Visit#', 'Date', 'Diagnosis', 'Medicine prescribed', 'Lab test requested'
        listBox = ttk.Treeview(self.frm_patiant_history, columns=cols, show='headings', selectmode='browse')

        # set column headings

        listBox.heading(cols[0], text=cols[0])
        listBox.column(cols[0], minwidth=60, width=60, anchor=tk.CENTER)
        listBox.heading(cols[1], text=cols[1])
        listBox.column(cols[1], minwidth=100, width=100, anchor=tk.CENTER)
        for col in cols[2:]:
            listBox.heading(col, text=col)
            listBox.column(col, minwidth=80, width=240, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(self.frm_patiant_history, orient="vertical", command=listBox.yview)
        vsb.place(relx=.966, rely=1 / 16, height=600)

        listBox.configure(yscrollcommand=vsb.set)

        listBox.place(relx=.02, rely=1 / 16, height=600, width=870)

        ttk.Button(self.frm_patiant_history, text='Check', command=lambda: self.check_history(p_id.get(), listBox)) \
            .place(relx=.22, rely=.15 / 16, anchor='nw', width=90, height=30)

        ttk.Button(self.frm_patiant_history, text='Clear', command=lambda: self.clear_table(listBox)) \
            .place(relx=.33, rely=.15 / 16, anchor='nw', width=90, height=30)

        pass

    def check_history(self, pid, listBox):
        if not pid:
            mb.showwarning("Error", "Patient ID is required")
            return

        results = list(db().getConn().execute(f"select s_date, diag, medicine, lab_test from private.session "
                                              f"where u_id = {self.employee.id} and p_id = {pid} order by s_date;"))

        if not results:
            mb.showwarning("Error", f"No Data found for patient {pid} in the system")
            return


        for idx, item in enumerate(results):
            listBox.insert("", "end", values=(idx, item[0], item[1], item[2], item[3]))
            pass

        pass

    def clear_table(self, listBox):
        listBox.delete(*listBox.get_children())

