import mysql.connector as sql
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from time import strftime
import random
mydb=sql.connect(host="localhost",user="root",passwd="admin",database="health_hospital")
mycur=mydb.cursor()

def create_table():
    """To Create Tables in Database"""
    mycur.execute('create table hosp_details(g_bed int(2), icu_room int(2), special_room int(2))')
    mycur.execute('create table patient_details(p_id char(4) primary key,p_name char(25) ,p_age int(3),p_problems char(40),\
    p_phono char(10), days int(2), room char(15), room_no int(3), Total_Bill float(10))')
    mycur.execute('create table doctor_details(d_name char(25) primary key,d_age int(3),d_department char(40),d_phono char(10))')
    mycur.execute('create table worker_details(w_name char(25) primary key,w_age int(3),w_workname char(40),w_phono char(10))')
    mycur.execute('create table patient_details_opd(p_id char(4) primary key,p_name char(25) ,p_age int(3),p_problems char(40),\
    p_phono char(10), Total_Bill float(10))')
    mydb.commit()
    messagebox.showinfo("Alert", "Tables Created")

def Insert_Hosp():
    """To insert data into Hospital Database"""
    # GUIconfig
    hosp = Tk()
    hosp.title("Insert Hospital Records")

    # Commands
    def getdata():
        g_beds = e1.get()
        icu_room = e2.get()
        special_room = e3.get()
        try:
            mycur.execute("truncate table hosp_details")  #Will delete previous bed data
            mydb.commit()
            mycur.execute("insert into hosp_details values({},{},{})".format(g_beds, icu_room, special_room))
            mydb.commit()
            messagebox.showinfo("Alert", "Record Submitted")
            beddata()
            updatebeddata()
        except:
            er = "Some Error May have Occured, Please recheck"
            messagebox.showinfo("Alert", er)


    # Label Fields
    cd1 = Label(hosp, text="Enter No.of General Beds", font="Arial")
    cd2 = Label(hosp, text="Enter No.of ICU Rooms", font="Arial")
    cd3 = Label(hosp, text="Enter No.of Special Rooms", font="Arial")

    cd1.grid(row=0, column=0)
    cd2.grid(row=1, column=0)
    cd3.grid(row=2, column=0)

    # Entry Fields
    e1 = Entry(hosp, textvariable=IntVar)
    e2 = Entry(hosp, textvariable=IntVar)
    e3 = Entry(hosp, textvariable=IntVar)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    # button
    Submit_button = Button(hosp, text="Submit", command=getdata)
    Submit_button.grid(row=5, column=0)

    mainloop()

def Update_Hosp_S():
    """To delete a special bed from database as it is booked by patient"""
    mycur.execute("update hosp_details set special_room=special_room-1")
    mydb.commit()
    updatebeddata()

def Update_Hosp_ICU():
    """To delete an ICU bed from database as it is booked by patient"""
    mycur.execute("update hosp_details set icu_room=icu_room-1")
    mydb.commit()
    updatebeddata()

def Update_Hosp_GEN():
    """To delete a general bed from database as it is booked by patient"""     
    mycur.execute("update hosp_details set g_bed=g_bed-1")
    mydb.commit()
    updatebeddata()

              
def Insert_Doctors():
    """To enter doctors data in database"""
    # GUIconfig
    doct = Tk()
    doct.title("Insert Doctor Records")

    # Commands
    def getdata():
        """To get data inserted by user in text field"""
        def allcheck():
            """TO check whether data inserted have general errors or not"""
            a=True
            if len(e4.get()) != 10:
                messagebox.showerror("Alert", "Please Enter 10 Digit Number")
                a = False
            if e2.get()==0:
                messagebox.showerror("Alert", "Please Enter Correct Age")
                a = False
            return a

        if allcheck()==True:
            d_name = e1.get()
            d_age = e2.get()
            d_department = e3.get()
            d_phono = e4.get()
            try:
                mycur.execute("insert into doctor_details values('{}',{},'{}','{}')".format(d_name,d_age,d_department,d_phono))
                mydb.commit()
                messagebox.showinfo("Alert", "Record Submitted")
            except:
                er = "Some Error May have Occured, Please recheck"
                messagebox.showinfo("Alert", er)
        else:
            pass

    # Label Fields
    cd1 = Label(doct, text="Enter Doctor Name :", font="Arial").grid(row=0, column=0)
    cd2 = Label(doct, text="Enter Age         :", font="Arial").grid(row=1, column=0)
    cd3 = Label(doct, text="Enter Department  :", font="Arial").grid(row=2, column=0)
    cd4 = Label(doct, text="Enter Phone No.   :", font="Arial").grid(row=3, column=0)


    # Entry Fields
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()
    var4 = StringVar()
    e1 = Entry(doct,   textvariable=var1)
    e2 = Entry(doct,   textvariable=var2)
    e3 = Entry(doct,   textvariable=var3)
    e4 = Entry(doct,   textvariable=var4)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)

    # button
    Submit_button = Button(doct, text="Submit",   command=getdata)
    Submit_button.grid(row=5, column=0)

    mainloop()

def Insert_Patient():
    """To enter patient data in database"""
    pat = Tk()
    pat.title("Insert Patients")

    def submit():
        def select_room():
            r_choice = 0
            r_no=0
            if menu.get()==options[0]:
                Update_Hosp_GEN()
                g_ex_lt = []
                mycur.execute("Select * from patient_details")
                for x in mycur:
                    l = x[7]
                    g_ex_lt.append(l)

                a=True
                while a:
                    r_choice = random.choice(g_list)
                    if r_choice in g_ex_lt:
                        a=True
                    else:
                        a=False
                r_no = int(r_choice)

            elif menu.get()==options[1]:
                Update_Hosp_ICU()
                g_ex_lt = []
                mycur.execute("Select * from patient_details")
                for x in mycur:
                    l = x[7]
                    g_ex_lt.append(l)

                a=True
                while a:
                    r_choice = random.choice(i_list)
                    if r_choice in g_ex_lt:
                        a=True
                    else:
                        a=False
                r_no = int(r_choice)

            elif menu.get()==options[2]:
                Update_Hosp_S()
                g_ex_lt = []
                mycur.execute("Select * from patient_details")
                for x in mycur:
                    l = x[7]
                    g_ex_lt.append(l)

                a=True
                while a:
                    r_choice = random.choice(s_list)
                    if r_choice in g_ex_lt:
                        a=True
                    else:
                        a=False
                r_no = int(r_choice)

            return r_no

        def bed_bill():
            b_bill = 0
            if menu.get()==options[0]:
                b_bill = int(sb1.get()) * 1000
            elif menu.get()==options[1]:
                b_bill = int(sb1.get()) * 1500
            elif menu.get()==options[2]:
                b_bill = int(sb1.get()) * 2000
            return b_bill

        def allcheck():
            a=True
            if menu.get()==options[0]:
                if g_beds==0:
                    messagebox.showerror("Error", "Sorry:( No General Beds Availaible")
                    a=False
            elif menu.get() == options[1]:
                if i_beds==0:
                    messagebox.showerror("Error", "Sorry:( No ICU Beds Availaible")
                    a=False
            elif menu.get()==options[2]:
                if s_beds==0:
                    messagebox.showerror("Error", "Sorry:( No Special Beds Availaible")
                    a=False
            if len(e5.get())!=10:
                messagebox.showerror("Error", "Please Enter 10 Digit Number")
                a = False
            if e3.get()==0:
                messagebox.showerror("Error", "Please Enter Correct Age")
                a = False
            return a

        if allcheck()==True:
            r_final = select_room()
            t_bill = int(e8.get()) + int(e9.get()) + bed_bill()
            try:
                mycur.execute("insert into patient_details values('{}','{}',{},'{}','{}',{},'{}',{},{})".format(e1.get(), e2.get(),e3.get(), e4.get(), e5.get(), sb1.get(), menu.get(), r_final, t_bill))
                mydb.commit()
                alert_msg="Record submitted succesfully, Total Bill is: " + str(t_bill)
                messagebox.showinfo("Alert", alert_msg)
            except Exception as e:
                er = "Some Error May have Occured, Please recheck"
                messagebox.showerror("Error", e)
        else:
            pass

    cd1 = Label(pat, text="Enter Patient Id     :", font="Arial").grid(row=0, column=0)
    cd2 = Label(pat, text="Enter Patient Name   :", font="Arial").grid(row=1, column=0)
    cd3 = Label(pat, text="Enter Patient Age    :", font="Arial").grid(row=2, column=0)
    cd4 = Label(pat, text="Enter Patient Problem:", font="Arial").grid(row=3, column=0)
    cd5 = Label(pat, text="Enter Patient Contact", font="Arial").grid(row=4, column=0)
    cd6 = Label(pat, text="Type of Bed          :", font="Arial").grid(row=5, column=0)
    cd7 = Label(pat, text="No.of Days           :", font="Arial").grid(row=6, column=0)
    cd8 = Label(pat, text="Medicine Charges     :", font="Arial").grid(row=7, column=0)
    cd9= Label(pat, text="Consultant Charges   :", font="Arial").grid(row=8, column=0)


    e1 = Entry(pat, textvariable=StringVar)
    e2 = Entry(pat, textvariable=StringVar)
    e3 = Entry(pat, textvariable=IntVar)
    e4 = Entry(pat, textvariable=StringVar)
    e5 = Entry(pat, textvariable=StringVar)
    e8 = Entry(pat, textvariable=IntVar)
    e9 = Entry(pat, textvariable=IntVar)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e8.grid(row=7, column=1)
    e9.grid(row=8, column=1)

    #MENU
    menu = StringVar(pat)
    options = ["General Bed", "ICU Bed", "Special Bed"]
    mn1 = OptionMenu(pat, menu, options[0], *options)
    mn1.grid(row=5,column=1)

    #SpinBox
    sb1 = Spinbox(pat, from_=0, to=100)
    sb1.grid(row=6, column=1)

    bt1 = Button(pat, text="Submit", command=submit).grid(row=9, column=0)
    
def Insert_Patient_OPD():
    """To enter opd patient data in database"""
    pat = Tk()
    pat.title("Insert OPD Patients")
    
    def submit():
        def allcheck():
            a=True
            if len(e5.get())!=10:
                messagebox.showerror("Error", "Please Enter 10 Digit Number")
                a = False
            if e3.get()==0:
                messagebox.showerror("Error", "Please Enter Correct Age")
                a = False
            return a

        if allcheck()==True:
            t_bill = int(e8.get()) + int(e9.get())
            try:
                mycur.execute("insert into patient_details_opd values('{}','{}',{},'{}','{}',{})".format(e1.get(), e2.get(),e3.get(), e4.get(), e5.get(), t_bill))
                mydb.commit()
                alert_msg="Record submitted succesfully, Total Bill is: " + str(t_bill)
                messagebox.showinfo("Alert", alert_msg)
            except Exception as e:
                er = "Some Error May have Occured, Please recheck"
                messagebox.showerror("Error", e)
        else:
            pass
    
    cd1 = Label(pat, text="Enter Patient Id     :", font="Arial").grid(row=0, column=0)
    cd2 = Label(pat, text="Enter Patient Name   :", font="Arial").grid(row=1, column=0)
    cd3 = Label(pat, text="Enter Patient Age    :", font="Arial").grid(row=2, column=0)
    cd4 = Label(pat, text="Enter Patient Problem:", font="Arial").grid(row=3, column=0)
    cd5 = Label(pat, text="Enter Patient Contact", font="Arial").grid(row=4, column=0)
    cd8 = Label(pat, text="Medicine Charges     :", font="Arial").grid(row=7, column=0)
    cd9= Label(pat, text="Consultant Charges   :", font="Arial").grid(row=8, column=0)


    e1 = Entry(pat, textvariable=StringVar)
    e2 = Entry(pat, textvariable=StringVar)
    e3 = Entry(pat, textvariable=IntVar)
    e4 = Entry(pat, textvariable=StringVar)
    e5 = Entry(pat, textvariable=StringVar)
    e8 = Entry(pat, textvariable=IntVar)
    e9 = Entry(pat, textvariable=IntVar)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e8.grid(row=7, column=1)
    e9.grid(row=8, column=1)

    bt1 = Button(pat, text="Submit", command=submit).grid(row=9, column=0)

def Insert_Workers():
    wrks = Tk()
    wrks.title("Insert Workers")

    def getdata():
        def allcheck():
            a=True
            if len(e3.get()) != 10:
                messagebox.showerror("Error", "Please Enter 10 Digit Number")
                a = False
            if e2.get()==0:
                messagebox.showerror("Error", "Please Enter Correct Age")
                a = False
            return a
        w_name = e1.get()
        w_age = e2.get()
        w_phono = e3.get()
        w_workname=""
        if radio.get()==1:
            w_workname = "Nurse"
        if radio.get()==2:
            w_workname = "Receptionist"
        if radio.get()==3:
            w_workname = "Compounder"
        if radio.get()==4:
            w_workname = "Sweeper"
        if radio.get()==5:
            w_workname = "Pharamacist"
        mycur.execute("insert into worker_details values('{}',{},'{}','{}')".format(w_name, w_age, w_workname, w_phono))
        mydb.commit()

        messagebox.showinfo("Alert", "Record Submitted")


    
    cd1 = Label(wrks, text="Enter Worker Name   : ", font="Arial").grid(row=0, column=0)
    cd1 = Label(wrks, text="Enter Worker Age    : ", font="Arial").grid(row=1, column=0)
    cd1 = Label(wrks, text="Enter Worker Contact: ", font="Arial").grid(row=2, column=0)

    e1 = Entry(wrks, textvariable=StringVar)
    e2 = Entry(wrks, textvariable=StringVar)
    e3 = Entry(wrks, textvariable=StringVar)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    #RadioButton
    radio = IntVar(wrks)
    rd1 = Radiobutton(wrks, text="Nurse", variable=radio, value=1)
    rd2 = Radiobutton(wrks, text="Receptionist", variable=radio, value=2)
    rd3 = Radiobutton(wrks, text="Compounder", variable=radio, value=3)
    rd4 = Radiobutton(wrks, text="Sweeper", variable=radio, value=4)
    rd5 = Radiobutton(wrks, text="Pharamacist", variable=radio, value=5)

    rd1.grid(row=3, column=0)
    rd2.grid(row=3, column=1)
    rd3.grid(row=4, column=0)
    rd4.grid(row=4, column=1)
    rd5.grid(row=5, column=0)

    submit = Button(wrks, text="Submit",command=getdata)
    submit.grid(row=6,column=0)


    mainloop()

def Display_Hosp():
    hosp_d = Tk()
    hosp_d.title("Hospital Details")
    
    cd1 = Label(hosp_d, text="Enter No.of General Beds", font="Arial").grid(row=0, column=0)
    cd2 = Label(hosp_d, text="Enter No.of ICU Rooms", font="Arial").grid(row=1, column=0)
    cd3 = Label(hosp_d, text="Enter No.of Special Rooms", font="Arial").grid(row=2, column=0)
    
    e1 = Entry(hosp_d, textvariable=StringVar)
    e2 = Entry(hosp_d, textvariable=StringVar)
    e3 = Entry(hosp_d, textvariable=StringVar)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    mycur.execute("Select * from hosp_details")
    for x in mycur:           
        e1.insert(0, x[0])
        e2.insert(0, x[1])
        e3.insert(0, x[2])
    mainloop()

            
def Search_Records_Doctors():
    srch = Tk()
    srch.title("Search Records")

    def getdata():
        for item in treev.get_children():
            treev.delete(item)

        dname_list = []
        dage_list = []
        dd_list = []
        dp_list = []



        mycur.execute("Select * from doctor_details where d_name='{}'".format(e1.get()))
        for x in mycur:
            dname_list.append(x[0])
            dage_list.append(x[1])
            dd_list.append(x[2])
            dp_list.append(x[3])

        for i in range(0, len(dname_list)):
            treev.insert("", 'end', text="L1",values=(dname_list[i], dage_list[i], dd_list[i], dp_list[i]))

    def showall():
        dname_list = []
        dage_list = []
        dd_list = []
        dp_list = []


        mycur.execute("Select * from doctor_details".format(e1.get()))
        for x in mycur:
            dname_list.append(x[0])
            dage_list.append(x[1])
            dd_list.append(x[2])
            dp_list.append(x[3])

        for i in range(0, len(dname_list)):
            treev.insert("", 'end', text="L1", values=(dname_list[i], dage_list[i], dd_list[i], dp_list[i]))

    def modify():
        srchm = Tk()
        srchm.title("Modify Data")
        where = treev.item(treev.selection()[0])['values'][0]

        def tdata():
            s = treev.selection()[0]
            me1.insert(0, treev.item(s)['values'][0])
            me2.insert(0, treev.item(s)['values'][1])
            me3.insert(0, treev.item(s)['values'][2])
            me4.insert(0, treev.item(s)['values'][3])


        def modifym():
            try:
                mycur.execute("update doctor_details set d_name='{}', d_age={}, d_department='{}', d_phono='{}' where d_name = '{}'".format(me1.get(), me2.get(), me3.get(), me4.get(), where))
                mydb.commit()
                messagebox.showinfo("Alert", "Record Succesfully Updated")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "There is Some Error please recheck")

        ml1 = Label(srchm, text="Doctor Name: ", font="Arial").grid(row=0, column=0)
        ml2 = Label(srchm, text="Doctor Age : ", font="Arial").grid(row=1, column=0)
        ml3 = Label(srchm, text="Department : ", font="Arial").grid(row=2, column=0)
        ml4 = Label(srchm, text="Contact No : ", font="Arial").grid(row=3, column=0)

        me1 = Entry(srchm, textvariable=StringVar)
        me2 = Entry(srchm, textvariable=IntVar)
        me3 = Entry(srchm, textvariable=StringVar)
        me4 = Entry(srchm, textvariable=StringVar)


        me1.grid(row=0, column=1)
        me2.grid(row=1, column=1)
        me3.grid(row=2, column=1)
        me4.grid(row=3, column=1)

        tdata()

        bt5 = Button(srchm, text="Modify", command=modifym)
        bt5.grid(row=4, column=0)

        mainloop()

    def delete():
        name = treev.item(treev.selection()[0])['values'][0]

        answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete selected record")
        if answer:
            try:
                mycur.execute("delete from doctor_details where d_name='{}'".format(name))
                mydb.commit()
                messagebox.showinfo("Alert", "Selected Record Deleted")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "Sorry we cant delete please try again")

    e1 = Entry(srch, textvariable=StringVar)

    """TreeView Widget"""
    treev = Treeview(srch, selectmode='browse')

    treev.grid(row=1, column=0, columnspan=3)


    verscrlbar = Scrollbar(srch,
                           orient="vertical",
                           command=treev.yview)

    verscrlbar.grid(row=1, column=4)


    treev.configure(xscrollcommand=verscrlbar.set)


    treev["columns"] = ("1", "2", "3", "4")


    treev['show'] = 'headings'


    treev.column("1", width=90, anchor='c')
    treev.column("2", width=90, anchor='se')
    treev.column("3", width=90, anchor='se')
    treev.column("4", width=90, anchor='se')


    treev.heading("1", text="Name")
    treev.heading("2", text="Age")
    treev.heading("3", text="Department")
    treev.heading("4", text="Contact")

    lb1 = Label(srch, text="Doctor Name", font="Arial")

    lb1.grid(row=0, column=0)
    e1.grid(row=0, column=1)

    #Button
    bt1 = Button(srch, text="Search", command=getdata)
    bt2 = Button(srch, text="Show All", command=showall)
    bt3 = Button(srch, text="Modify Data", command=modify)
    bt4 = Button(srch, text="Delete Data", command=delete)

    bt1.grid(row=0, column=2)
    bt2.grid(row=2, column=0)
    bt3.grid(row=2, column=1)
    bt4.grid(row=2, column=2)

    mainloop()

def Search_Records_Patient():
    srch = Tk()
    srch.title("Search Records")

    def getdata():
        for item in treev.get_children():
            treev.delete(item)

        pid_list = []
        pname_list = []
        page_list = []
        pproblems_list = []
        pcontact=[]
        pday = []
        proomt = []
        proomn = []
        ptbill = []


        mycur.execute("Select * from patient_details where p_id='{}'".format(e1.get()))
        for x in mycur:
            pid_list.append(x[0])
            pname_list.append(x[1])
            page_list.append(x[2])
            pproblems_list.append(x[3])
            pcontact.append(x[4])
            pday.append(x[5])
            proomt.append(x[6])
            proomn.append(x[7])
            ptbill.append(x[8])


        for i in range(0, len(pid_list)):
            treev.insert("", 'end', text="L1", values=(pid_list[i], pname_list[i], page_list[i], pproblems_list[i], pcontact[i], pday[i], proomt[i], proomn[i], ptbill[i]))

    def showall():
        for item in treev.get_children():
            treev.delete(item)

        pid_list = []
        pname_list = []
        page_list = []
        pproblems_list = []
        pcontact = []
        pday = []
        proomt = []
        proomn = []
        ptbill = []


        mycur.execute("Select * from patient_details".format(e1.get()))
        for x in mycur:
            pid_list.append(x[0])
            pname_list.append(x[1])
            page_list.append(x[2])
            pproblems_list.append(x[3])
            pcontact.append(x[4])
            pday.append(x[5])
            proomt.append(x[6])
            proomn.append(x[7])
            ptbill.append(x[8])

        for i in range(0, len(pid_list)):
            treev.insert("", 'end', text="L1", values=(
            pid_list[i], pname_list[i], page_list[i], pproblems_list[i], pcontact[i], pday[i], proomt[i], proomn[i],
            ptbill[i]))

    def modify():
        srchm = Tk()
        srchm.title("Modify Data")
        where = treev.item(treev.selection()[0])['values'][0]

        def tdata():
            s = treev.selection()[0]
            me1.insert(0, treev.item(s)['values'][0])
            me2.insert(0, treev.item(s)['values'][1])
            me3.insert(0, treev.item(s)['values'][2])
            me4.insert(0, treev.item(s)['values'][3])
            me5.insert(0, treev.item(s)['values'][4])
            me6.insert(0, treev.item(s)['values'][5])
            me7.insert(0, treev.item(s)['values'][6])
            me8.insert(0, treev.item(s)['values'][7])

        def modifym():
            try:
                mycur.execute(
                    "update patient_details set p_id='{}', p_name='{}', p_age={}, p_problems='{}', p_phono='{}', days={}, room='{}', room_no={}, Total_Bill={} where p_id = '{}'".format(
                        me1.get(), me2.get(), me3.get(), me4.get(), me5.get(), me6.get(), me7.get(), me8.get(), me9.get(), where))
                mydb.commit()
                messagebox.showinfo("Alert", "Record Succesfully Updated")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "There is Some Error please recheck")

        ml1 = Label(srchm, text="ID          : ", font="Arial").grid(row=0, column=0)
        ml2 = Label(srchm, text="Name        : ", font="Arial").grid(row=1, column=0)
        ml3 = Label(srchm, text="Age         : ", font="Arial").grid(row=2, column=0)
        ml4 = Label(srchm, text="Problems    : ", font="Arial").grid(row=3, column=0)
        ml5 = Label(srchm, text="Contact     : ", font="Arial").grid(row=4, column=0)
        ml6 = Label(srchm, text="Days        : ", font="Arial").grid(row=5, column=0)
        ml7 = Label(srchm, text="RoomType    : ", font="Arial").grid(row=6, column=0)
        ml8 = Label(srchm, text="RoomNo      : ", font="Arial").grid(row=7, column=0)
        ml9 = Label(srchm, text="Total Bill  : ", font="Arial").grid(row=8, column=0)

        me1 = Entry(srchm, textvariable=StringVar)
        me2 = Entry(srchm, textvariable=StringVar)
        me3 = Entry(srchm, textvariable=IntVar)
        me4 = Entry(srchm, textvariable=StringVar)
        me5 = Entry(srchm, textvariable=StringVar)
        me6 = Entry(srchm, textvariable=IntVar)
        me7 = Entry(srchm, textvariable=StringVar)
        me8 = Entry(srchm, textvariable=IntVar)
        me9 = Entry(srchm, textvariable=IntVar)

        me1.grid(row=0, column=1)
        me2.grid(row=1, column=1)
        me3.grid(row=2, column=1)
        me4.grid(row=3, column=1)
        me5.grid(row=4, column=1)
        me6.grid(row=5, column=1)
        me7.grid(row=6, column=1)
        me8.grid(row=7, column=1)
        me9.grid(row=8, column=1)

        tdata()

        bt5 = Button(srchm, text="Modify", command=modifym)
        bt5.grid(row=9, column=0)

        mainloop()

    def delete():
        name = treev.item(treev.selection()[0])['values'][0]

        answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete selected record")
        if answer:
            try:
                mycur.execute("delete from patient_details where p_id='{}'".format(name))
                mydb.commit()
                messagebox.showinfo("Alert", "Selected Record Deleted")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "Sorry we cant delete please try again")

    e1 = Entry(srch, textvariable=StringVar)

    """TreeView Widget"""
    treev = Treeview(srch, selectmode='browse')

    treev.grid(row=1, column=0, columnspan=3)

    verscrlbar = Scrollbar(srch,
                           orient="vertical",
                           command=treev.yview)

    verscrlbar.grid(row=1, column=4)

    treev.configure(xscrollcommand=verscrlbar.set)

    treev["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

    treev['show'] = 'headings'

    treev.column("1", width=90, anchor='c')
    treev.column("2", width=90, anchor='se')
    treev.column("3", width=90, anchor='se')
    treev.column("4", width=90, anchor='se')
    treev.column("5", width=90, anchor='se')
    treev.column("6", width=90, anchor='se')
    treev.column("7", width=90, anchor='se')
    treev.column("8", width=90, anchor='se')
    treev.column("9", width=90, anchor='se')

    treev.heading("1", text="ID")
    treev.heading("2", text="Name")
    treev.heading("3", text="Age")
    treev.heading("4", text="Problems")
    treev.heading("5", text="Contact")
    treev.heading("6", text="Days")
    treev.heading("7", text="Room Type")
    treev.heading("8", text="Room No.")
    treev.heading("9", text="Total Bill")

    lb1 = Label(srch, text="Patient ID", font="Arial")

    lb1.grid(row=0, column=0)
    e1.grid(row=0, column=1)

    # Button
    bt1 = Button(srch, text="Search", command=getdata)
    bt2 = Button(srch, text="Show All", command=showall)
    bt3 = Button(srch, text="Modify Data", command=modify)
    bt4 = Button(srch, text="Delete Data", command=delete)

    bt1.grid(row=0, column=2)
    bt2.grid(row=2, column=0)
    bt3.grid(row=2, column=1)
    bt4.grid(row=2, column=2)

    mainloop()
    
def Search_Records_Patient_OPD():
    srch = Tk()
    srch.title("Search OPD Patient Records")

    def getdata():
        for item in treev.get_children():
            treev.delete(item)

        pid_list = []
        pname_list = []
        page_list = []
        pproblems_list = []
        pcontact=[]
        ptbill = []


        mycur.execute("Select * from patient_details_opd where p_id='{}'".format(e1.get()))
        for x in mycur:
            pid_list.append(x[0])
            pname_list.append(x[1])
            page_list.append(x[2])
            pproblems_list.append(x[3])
            pcontact.append(x[4])
            ptbill.append(x[8])


        for i in range(0, len(pid_list)):
            treev.insert("", 'end', text="L1", values=(pid_list[i], pname_list[i], page_list[i], pproblems_list[i], pcontact[i], ptbill[i]))

    def showall():
        for item in treev.get_children():
            treev.delete(item)

        pid_list = []
        pname_list = []
        page_list = []
        pproblems_list = []
        pcontact = []
        ptbill = []


        mycur.execute("Select * from patient_details_opd".format(e1.get()))
        for x in mycur:
            pid_list.append(x[0])
            pname_list.append(x[1])
            page_list.append(x[2])
            pproblems_list.append(x[3])
            pcontact.append(x[4])
            ptbill.append(x[8])

        for i in range(0, len(pid_list)):
            treev.insert("", 'end', text="L1", values=(
            pid_list[i], pname_list[i], page_list[i], pproblems_list[i], pcontact[i], ptbill[i]))

    def modify():
        srchm = Tk()
        srchm.title("Modify Data")
        where = treev.item(treev.selection()[0])['values'][0]

        def tdata():
            s = treev.selection()[0]
            me1.insert(0, treev.item(s)['values'][0])
            me2.insert(0, treev.item(s)['values'][1])
            me3.insert(0, treev.item(s)['values'][2])
            me4.insert(0, treev.item(s)['values'][3])
            me5.insert(0, treev.item(s)['values'][4])

        def modifym():
            try:
                mycur.execute(
                    "update patient_details_opd set p_id='{}', p_name='{}', p_age={}, p_problems='{}', p_phono='{}',  Total_Bill={} where p_id = '{}'".format(
                        me1.get(), me2.get(), me3.get(), me4.get(), me5.get(), me9.get(), where))
                mydb.commit()
                messagebox.showinfo("Alert", "Record Succesfully Updated")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "There is Some Error please recheck")

        ml1 = Label(srchm, text="ID          : ", font="Arial").grid(row=0, column=0)
        ml2 = Label(srchm, text="Name        : ", font="Arial").grid(row=1, column=0)
        ml3 = Label(srchm, text="Age         : ", font="Arial").grid(row=2, column=0)
        ml4 = Label(srchm, text="Problems    : ", font="Arial").grid(row=3, column=0)
        ml5 = Label(srchm, text="Contact     : ", font="Arial").grid(row=4, column=0)
        ml9 = Label(srchm, text="Total Bill  : ", font="Arial").grid(row=8, column=0)

        me1 = Entry(srchm, textvariable=StringVar)
        me2 = Entry(srchm, textvariable=StringVar)
        me3 = Entry(srchm, textvariable=IntVar)
        me4 = Entry(srchm, textvariable=StringVar)
        me5 = Entry(srchm, textvariable=StringVar)
        me9 = Entry(srchm, textvariable=IntVar)

        me1.grid(row=0, column=1)
        me2.grid(row=1, column=1)
        me3.grid(row=2, column=1)
        me4.grid(row=3, column=1)
        me5.grid(row=4, column=1)
        me9.grid(row=8, column=1)

        tdata()

        bt5 = Button(srchm, text="Modify", command=modifym)
        bt5.grid(row=9, column=0)

        mainloop()

    def delete():
        name = treev.item(treev.selection()[0])['values'][0]

        answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete selected record")
        if answer:
            try:
                mycur.execute("delete from patient_details where p_id='{}'".format(name))
                mydb.commit()
                messagebox.showinfo("Alert", "Selected Record Deleted")
                for item in treev.get_children():
                    treev.delete(item)
                showall()
            except:
                messagebox.showerror("Error", "Sorry we cant delete please try again")

    e1 = Entry(srch, textvariable=StringVar)

    """TreeView Widget"""
    treev = Treeview(srch, selectmode='browse')

    treev.grid(row=1, column=0, columnspan=3)

    verscrlbar = Scrollbar(srch,
                           orient="vertical",
                           command=treev.yview)

    verscrlbar.grid(row=1, column=4)

    treev.configure(xscrollcommand=verscrlbar.set)

    treev["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

    treev['show'] = 'headings'

    treev.column("1", width=90, anchor='c')
    treev.column("2", width=90, anchor='se')
    treev.column("3", width=90, anchor='se')
    treev.column("4", width=90, anchor='se')
    treev.column("5", width=90, anchor='se')
    treev.column("6", width=90, anchor='se')

    treev.heading("1", text="ID")
    treev.heading("2", text="Name")
    treev.heading("3", text="Age")
    treev.heading("4", text="Problems")
    treev.heading("5", text="Contact")
    treev.heading("6", text="Total Bill")

    lb1 = Label(srch, text="Patient ID", font="Arial")

    lb1.grid(row=0, column=0)
    e1.grid(row=0, column=1)

    # Button
    bt1 = Button(srch, text="Search", command=getdata)
    bt2 = Button(srch, text="Show All", command=showall)
    bt3 = Button(srch, text="Modify Data", command=modify)
    bt4 = Button(srch, text="Delete Data", command=delete)

    bt1.grid(row=0, column=2)
    bt2.grid(row=2, column=0)
    bt3.grid(row=2, column=1)
    bt4.grid(row=2, column=2)

    mainloop()

def Deleteall():
    answer = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete all record?")
    if answer:
        try:
            mycur.execute("truncate table hosp_details")
            mycur.execute("truncate table doctor_details")
            mycur.execute("truncate table patient_details")
            mycur.execute("truncate table worker_details")
            mydb.commit()
            messagebox.showinfo("Alert", "All Table Record Deleted")
        except:
            messagebox.showerror("Error", "Sorry we cant delete please try again")
def updatebeddata():
    for item in treev.get_children():
        treev.delete(item)
    treev.insert("", 'end', text="L1", values=(g_beds, i_beds, s_beds))

def time():
    string = strftime('%H:%M:%S %p')
    clk.config(text=string)
    clk.after(1000, time)
    
def beddata():
    global g_beds
    global s_beds
    global i_beds
    global g_list
    global s_list
    global i_List
    try:
        mycur.execute("Select * from hosp_details")
        g_beds = 0
        s_beds=0
        i_beds=0
        for x in mycur:
            g_beds=x[0]
            s_beds=x[1]
            i_beds=x[2]
        
        g_list = []
        s_list = []
        i_list = []
        for i in range(1, g_beds+1):
            g_list.append(100+i)
        for i in range(1, s_beds+1):
            s_list.append(200+i)
        for i in range(1, i_beds+1):
            i_list.append(300+i)
    except:
        g_beds = 0
        s_beds=0
        i_beds=0
        
        g_list = []
        s_list = []
        i_list = []
    

#---------------Menu -------------
# importing only  those functions 
# which are needed
# creating tkinter window
root = Tk()
root.title('Health Hospital')
root.geometry("510x400")
root.configure(background='#ec8833')
  
# Creating Menubar
menubar = Menu(root)
table = Menu(menubar, tearoff = 0)
table.add_command(label ='Create Tables', command = create_table)
sub_menu = Menu(table, tearoff=0)
sub_menu.add_command(label='Hospital Records', command =Insert_Hosp )
sub_menu.add_command(label='Doctors Records',command =Insert_Doctors)
sub_menu.add_command(label='Workers Records',command =Insert_Workers)
sub_sub_menu = Menu(sub_menu, tearoff=0)
sub_menu.add_cascade(label="Patient Records", menu=sub_sub_menu)
sub_sub_menu.add_command(label='Admit',command =Insert_Patient)
sub_sub_menu.add_command(label='OPD',command =Insert_Patient_OPD)
table.add_cascade(label="Insert",menu=sub_menu)
table.add_separator()
table.add_command(label ='Exit', command = root.destroy)
menubar.add_cascade(label="Create", menu=table)

#Search
table = Menu(menubar, tearoff = 0) # create the file_menu
sub_menu1 = Menu(table, tearoff=0)
sub_menu1.add_command(label="Doctor", command=Search_Records_Doctors)
sub_menu1.add_command(label="OPD", command=Search_Records_Patient_OPD)
sub_menu1.add_command(label="Admit", command=Search_Records_Patient)
table.add_cascade(label ='Search Data', menu=sub_menu1)
table.add_command(label ='Delete All', command = Deleteall)
menubar.add_cascade(label="Data",menu=table)


table = Menu(menubar, tearoff = 0)
table.add_command(label='Exit', command =root.destroy)
menubar.add_cascade(label="Exit",menu=table)

# MainWindow
clk = Label(root, font=('calibri', 15, 'bold'),background='#449bfa',foreground='white')
tt = Label(root,text="Welcome to Hospital Management System", font=('calibri', 15, 'bold'),background='#ec8833',foreground='#f1f94f')

#Treeview Beds Data
"""TreeView Widget"""
treev = Treeview(root, selectmode='browse')
treev.place(x=0, y=50)
verscrlbar = Scrollbar(root,orient="vertical",command=treev.yview)
verscrlbar.place(x=460, y=150)
treev.configure(xscrollcommand=verscrlbar.set)
treev["columns"] = ("1", "2", "3", "4")
treev['show'] = 'headings'

treev.column("1", width=90, anchor='c')
treev.column("2", width=90, anchor='se')
treev.column("3", width=90, anchor='se')

treev.heading("1", text="General Beds")
treev.heading("2", text="ICU Beds")
treev.heading("3", text="Special Beds")

# Beds Data
try:
    mycur.execute("Select * from hosp_details")
    g_beds = 0
    s_beds = 0
    i_beds = 0
    for x in mycur:
        g_beds = x[0]
        s_beds = x[1]
        i_beds = x[2]

    g_list = []
    s_list = []
    i_list = []
    for i in range(1, g_beds + 1):
        g_list.append(100 + i)
    for i in range(1, s_beds + 1):
        s_list.append(200 + i)
    for i in range(1, i_beds + 1):
        i_list.append(300 + i)
    updatebeddata()

except:
    g_beds = 0
    s_beds = 0
    i_beds = 0

    g_list = []
    s_list = []
    i_list = []
    updatebeddata()

tt.place(x=0, y=0)
clk.place(x=400, y=0)
time()

root.config(menu = menubar)
mainloop()
