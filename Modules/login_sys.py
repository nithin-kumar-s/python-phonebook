# Python 3.8.10 used as a version.

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter import ttk
import time
import sqlite3

# FUNCTIONS OF LOGIN SYSTEM

def check_login(event=None):
    """Checking the user login before opening
       the main application.
    """
    global usernm_entry
    usernm_entry_var = usernm_entry.get()
    password_var = passwod.get()
    conn_dbase = sqlite3.connect('/home/christian/Desktop/Chanbiy_CBook_project/CBook/Database/Db_Cb.db')
    curs_db = conn_dbase.cursor()
    data_exec = curs_db.execute('SELECT * FROM login_data')
    data = data_exec.fetchone()
    #for data in datas:
    if usernm_entry_var == data[0] and password_var == data[1]:
        CBook_app()
        usernm_entry.set('')
        passwod.set('')
    else:
        messagebox.showerror('CBook App error', \
                                    'Incorrect password.')

def activate_chk():
    """ It controls the Checkbutton 
        pressed by the used to show password.
    """
    if check_btn_state.get() == 1:
        passwrd_entry = Entry(username_lF, width=20, font='Arial 15', \
                                textvariable=passwod)
        passwrd_entry.grid(row=1, column=1, rowspan=2)
    else:
        passwrd_entry = Entry(username_lF, width=20, font='Arial 15', \
                        show='\u2022', textvariable=passwod)
        passwrd_entry.grid(row=1, column=1, rowspan=2)

# FUNCTIONS OF MAIN APPLICATION

def save_contact():
    """gets all entries from the users and 
       save them into the sqlite3 database.
    """
    # Variables store temporally data before
    # saving them into database.
    frst_ent = str(frst_nm_var.get())
    mid_ent = mid_nm_var.get()
    lst_ent = lst_nm_var.get()
    adr_con = addr_nm_entry.get('1.0', 'end')
    phn_ent = phn_nm_var.get()
    mail_ent = email_nm_var.get()
    
    # for Loop to clear all the available data of treeview.
    for child in treeview_dspl.get_children():
        treeview_dspl.delete(child)

    # Connecting to the sqlite database.
    conn_db = sqlite3.connect('/home/christian/Desktop/Chanbiy_CBook_project/CBook/Database/Db_Cb.db')
    cur_db = conn_db.cursor()
    queries = "INSERT INTO \
                    contact_info(first_name, middle_name,\
                        last_name, address, phone_number, \
                            email) values(?,?,?,?,?,?)"
    dat = (frst_ent,\
            mid_ent, lst_ent, adr_con, \
                phn_ent, mail_ent)
    cur_db.execute(queries, dat)
    queries_final_con = "SELECT * FROM contact_info"
    for data in cur_db.execute(queries_final_con):
        treeview_dspl.insert('', END, values=data)
    status_info.configure(text='Saved succefully.')
    conn_db.close()
    

    # Clearing all the field after saving data.
    frst_nm_var.set('')
    mid_nm_var.set('')
    lst_nm_var.set('')
    addr_nm_entry.delete("1.0", "end")
    phn_nm_var.set('')
    email_nm_var.set('')
    print("Data saved succefully.")
    

def reset_entries():
    ''' Gets all entries and clear them from
        each entries.
    '''
    frst_con = frst_nm_var.get()
    mid_con = mid_nm_var.get()
    lst_con = lst_nm_var.get()
    #adr_con = addr_nm_entry.get()
    phn_con = phn_nm_var.get()
    mail_con = email_nm_var.get()

    frst_nm_var.set('')
    mid_nm_var.set('')
    lst_nm_var.set('')
    addr_nm_entry.delete("1.0", "end")
    phn_nm_var.set('')
    email_nm_var.set('')

def search_contact():
    ''' Helps to find a wanted contact info.'''
    # for Loop to clear all the available data of treeview.
    for child in treeview_dspl.get_children():
        treeview_dspl.delete(child)

    name_res = search_var.get()
    conn_db = sqlite3.connect('/home/christian/Desktop/Chanbiy_CBook_project/CBook/Database/Db_Cb.db')
    cur_db = conn_db.cursor()
    queries = cur_db.execute("SELECT * FROM contact_info WHERE \
                first_name = (?)", (name_res,))
    list_res = []
    for result in queries:
        treeview_dspl.insert('', END, values = result)
        list_res.append(result)
    rslt_info.configure(text='Result : %s contact(s).' % (len(list_res)))
    cur_db.commit()
    conn_db.close()

def generate_file():
    """ generate a PDF File containing all the
        available contact in the database.
    """
    conn_db = sqlite3.connect('/home/christian/Desktop/Chanbiy_CBook_project/CBook/Database/Db_Cb.db')
    cur_db = conn_db.cursor()
    queries = "SELECT * FROM contact_info"
    data = cur_db.execute(queries)
    file_contact_info = open("/home/christian/Desktop/Chanbiy_CBook_project/CBook/Contact.txt", "w")
    for element in data.fetchall():
        file_contact_info.write(str(element))
        file_contact_info.write('/n')
    file_contact_info.close()
    conn_db.commit()
    conn_db.close()

def docs():
    ''' Contains documentation.'''
    doc_top = Toplevel(top_main_app)
    doc_top.geometry('300x100')
    doc_top.resizable(False, False)
    doc_top.title('CBook App - About')
    doc_lbl = Label(doc_top, text = "go to www.cbookapp.com",\
                    justify=CENTER)
    doc_lbl.grid()
    doc_top.mainloop()

def about_info():
    '''shows about of the main_app.'''
    abt_top = Toplevel(top_main_app)
    abt_top.geometry('300x100')
    abt_top.resizable(False, False)
    abt_top.title('CBook App - About')
    abt_lbl = Label(abt_top, text = "CBooK App by MY LEARNING POINT",\
                    justify=CENTER)
    abt_lbl.grid()
    abt_top.mainloop()


def logout_func():
    '''logs out the main application.'''
    askysno = askyesno('Confirmation',\
                        'Are you sure you want to log out ')
    if askysno:
        top_main_app.destroy()

# CBook App Main app
def CBook_app():
    """ Main application. """
    # Accessing to Top variable.
    global top_main_app #global top_main_app
    # Global variables for entries.
    global frst_nm_var
    global mid_nm_var
    global lst_nm_var
    global addr_nm_entry
    global phn_nm_var
    global email_nm_var
    global search_var
    global total_info
    global treeview_dspl
    global search_var 
    global rslt_info
    global status_info
    global wlm_usr_lbl

    top_main_app = Toplevel(log_gui) # Generating new window.
    top_main_app.title('CBook App v.1.0') # App title.
    top_main_app.geometry('800x580')
    top_main_app.resizable(False, False)

    frst_nm_var = StringVar()
    mid_nm_var = StringVar()
    lst_nm_var = StringVar()
    phn_nm_var = StringVar()
    email_nm_var = StringVar()
    search_var = StringVar()
    
    #MENUBAR OF THE APPLICATION
    menubar = Menu(top_main_app)
    # File option
    file_menu_stn = Menu(menubar, tearoff=0)
    file_menu_stn.add_command(label='Log out',\
                                command=logout_func)
    file_menu_stn.add_separator()
    file_menu_stn.add_command(label='Quit App',\
                                command=quit)
    menubar.add_cascade(label='File', menu=file_menu_stn)
    # Option.
    opt_menu_stn = Menu(menubar, tearoff=0)
    opt_menu_stn.add_command(label='Generate TXT File',\
                                command=generate_file)
    menubar.add_cascade(label='Option', menu=opt_menu_stn)       
    # Help.
    hlp_menu_stn = Menu(menubar, tearoff=0)
    hlp_menu_stn.add_command(label='Docs...',\
                                command=docs)
    hlp_menu_stn.add_command(label='About', \
                                command=about_info)
    menubar.add_cascade(label='Help', menu=hlp_menu_stn)    

    top_main_app.configure(menu=menubar)

# BODY OF THE MAIN APPLICATION
    # Welcome user Label + Button 
    wlm_usr_lbl= Label(top_main_app, fg="green", \
                    text="Welcome %s" % usernm_entry.get())
    wlm_usr_lbl.grid(row=0, column=1, columnspan=5)

    # LabelFrame container of user entries.
    lbl_dt_entry = LabelFrame(top_main_app,\
                    text='Contact Info')
    lbl_dt_entry.grid(row=1, column=0, padx=7, pady=7)
    # LabelFrame widgets.
    frst_nm = Label(lbl_dt_entry, text='First name', \
                     font='arial 14 bold')
    frst_nm.grid(row=0, column=0, \
                    sticky=W, padx=1, pady=1)
    frst_nm_entry = Entry(lbl_dt_entry, \
                    width=20, textvariable=frst_nm_var,\
                    font='arial 14 bold')
    frst_nm_entry.grid(row=0, column=1, padx=1, pady=1)
    midd_nm = Label(lbl_dt_entry, text='Middle name', \
                     font='arial 14 bold')
    midd_nm.grid(row=1, column=0, \
                    sticky=W, padx=1, pady=1)
    midd_nm_entry = Entry(lbl_dt_entry, \
                    width=20, textvariable=mid_nm_var,\
                    font='arial 14 bold')
    midd_nm_entry.grid(row=1, column=1, padx=1, pady=1)
    last_nm = Label(lbl_dt_entry, text='Last name', \
                     font='arial 14 bold')
    last_nm.grid(row=2, column=0, \
                    sticky=W, padx=1, pady=1)
    last_nm_entry = Entry(lbl_dt_entry, \
                    width=20, textvariable=lst_nm_var,\
                    font='arial 14 bold')
    last_nm_entry.grid(row=2, column=1, padx=1, pady=1)
    addr_nm = Label(lbl_dt_entry, text='Address', \
                     font='arial 14 bold')
    addr_nm.grid(row=3, column=0, \
                    sticky=W, padx=1, pady=1)
    addr_nm_entry = Text(lbl_dt_entry, 
                    width=20, height=2,
                    font='arial 14 bold')
    addr_nm_entry.grid(row=3, column=1, padx=1, pady=1)
    phone_nm = Label(lbl_dt_entry, text='Phone number', \
                     font='arial 14 bold')
    phone_nm.grid(row=4, column=0, \
                    sticky=W, padx=1, pady=1)
    phn_nm_entry = Entry(lbl_dt_entry, \
                    width=20, textvariable=phn_nm_var, \
                    font='arial 14 bold')
    phn_nm_entry.grid(row=4, column=1, padx=1, pady=1)
    mail_nm = Label(lbl_dt_entry, text='Email', \
                     font='arial 14 bold')
    mail_nm.grid(row=5, column=0, \
                    sticky=W, padx=1, pady=1)
    mail_nm_entry = Entry(lbl_dt_entry, \
                    width=20, textvariable=email_nm_var,\
                    font='arial 14 bold')
    mail_nm_entry.grid(row=5, column=1, padx=1, pady=1)


    # Label of save-reset buttons.
    lbl_sv_btn = LabelFrame(lbl_dt_entry)
    lbl_sv_btn.grid(row=6, column=1, columnspan=2)
    # Save-Reset buttons.
    save_btn = Button(lbl_sv_btn, text='Save',\
                    command=save_contact)
    save_btn.grid(row=0, column=0, padx=3, pady=3)
    reset_btn = Button(lbl_sv_btn, text='Reset',\
                    command=reset_entries)
    reset_btn.grid(row=0, column=1, padx=3, pady=3)

    # LabelFrame container of search bar and Treeview.
    lbl_dt_sch_trv = LabelFrame(top_main_app,\
                    text='Search bar')
    lbl_dt_sch_trv.grid(row=1, column=1)

    # LabelFrame search bar widgets.
    srch_bar = Entry(lbl_dt_sch_trv, width=25, \
                        font='arial 17 bold',
                        textvariable=search_var)
    srch_bar.grid(row=0, column=0, padx=7, pady=4)
    srch_bar_btn = Button(lbl_dt_sch_trv, text='Search',\
                    command=search_contact)
    srch_bar_btn.grid(row=0, column=1, padx=1)
    # Result searc status.
    rslt_info = Label(lbl_dt_sch_trv, fg='blue')
    rslt_info.grid(row=1, column=0)

#Separator Frame
    frame_sep = Frame(lbl_dt_sch_trv, height=170)
    frame_sep.grid()

# Status bar for displayng infos.
    status_info = Label(top_main_app, fg='green')
    status_info.grid(row=2, column=0)
    total_info = Label(top_main_app, fg='Blue')
    total_info.grid(row=3, column=0)

# Treeview for displaying recorded data.
    treeview_dspl = ttk.Treeview(top_main_app,\
                        show='headings')
    treeview_dspl['columns']=('First name', 'Midlle Name', \
        'Last name', 'Adress', 'Phone number', 'Email')

    treeview_dspl.heading('#1', text='First Name')
    treeview_dspl.heading('#2', text='Midlle Name')
    treeview_dspl.heading('#3', text='Last name')
    treeview_dspl.heading('#4', text='Adress')
    treeview_dspl.heading('#5', text='Phone number')
    treeview_dspl.heading('#6', text='Email')

    treeview_dspl.column('#1', width=127)
    treeview_dspl.column('#2', width=127)
    treeview_dspl.column('#3', width=127)
    treeview_dspl.column('#4', width=127)
    treeview_dspl.column('#5', width=127)
    treeview_dspl.column('#6', width=127)

    treeview_dspl.grid(row=4, column=0)
    treeview_dspl.place(x=10, y=340)

    # Scroll bar of Treeview.
    scrollbar = ttk.Scrollbar(top_main_app, orient=VERTICAL,\
                         command=treeview_dspl.yview)
    treeview_dspl.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=4, column=1)
    scrollbar.place(x=770, y=340)

    # Connecting to dabase and Inserting data in Treeview
    tre_conn_db = sqlite3.connect('/home/christian/Desktop/Chanbiy_CBook_project/CBook/Database/Db_Cb.db')
    cur_tre = tre_conn_db.cursor()
    queries = cur_tre.execute("SELECT * FROM contact_info")
    tot_list = [] # List to save temporally data.
    for data in queries:
        tot_list.append(data)
        treeview_dspl.insert('', END, values=data)
    total_info.configure(text='Records : %s contact(s)' %(len(tot_list)))
    tre_conn_db.close()
    



    top_main_app.mainloop()


# Root User Login Interface.
log_gui = Tk()
log_gui.title('CBook App v.1.0 - Login')
log_gui.geometry('340x175')
log_gui.resizable(False, False)

# Entries specials variables.
usernm_entry = StringVar()
passwod = StringVar()
check_btn_state = IntVar()

# Label frame container of username and passwd.
username_lF = LabelFrame(log_gui)
username_lF.grid(row=1, column=0, padx=10, pady=5)

# Username - password labels and entries.
username_lbl = Label(username_lF, text='Username :', \
                        font='Arial 12 bold')
username_lbl.grid(row=0, column=0)
username_entry = Entry(username_lF, width=20, font='Arial 15',\
                        textvariable=usernm_entry)
username_entry.grid(row=0, column=1, pady=4) # Spacing widgets.
passwrd_lbl = Label(username_lF, text='Password :', \
                        font='Arial 12 bold')
passwrd_lbl.grid(row=1, column=0, rowspan=2, pady=3)
passwrd_entry = Entry(username_lF, width=20, \
                    font='Arial 15', show='\u2022', 
                    textvariable=passwod)
passwrd_entry.grid(row=1, column=1, rowspan=2)
passwrd_entry.bind('<Return>', check_login)

# Checkbutton for displaying the password.
chkbtn_disp = Checkbutton(username_lF, text='Show password', \
                variable=check_btn_state, command=activate_chk)
chkbtn_disp.grid(row=3, column=1, pady=3)

# Button submission to log into the main App.
btn_submit = Button(username_lF, text='Log in', width=24,\
                        command=check_login)
btn_submit.grid(row=4, column=1, pady=3)

# Label that show login error.
lbl_status = Label(username_lF, fg='red')
lbl_status.grid(row=5, column=1, pady=3)

log_gui.mainloop()

# The end. :)