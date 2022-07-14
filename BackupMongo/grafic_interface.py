#!/usr/bin/python
from tkinter import *
import tkinter as tk
from tkinter import messagebox, Entry
from Backup_process.backup import *
from Restore_process.restore_index import *


window = Tk()

window.title('Welcome to BetoGeek')
window.geometry('700x350')
background = 'light grey'  # Color de Fondo

title_msg = 'Backup and restore database mongoDB'
lbl = Label(window, text=title_msg, font=('Arial Bold', 20))
lbl.place(x=30, y=8)

l1_message = 'Please, insert the corresponding data to make the Backup to your MongoDB database'
lbl1 = Label(window, text=l1_message, font=('Arial Bold', 10))
lbl1.place(x=30, y=48)


#-------------------source data---------------------

l2_message = 'Data to Backup'
lbl0 = Label(window, text=l2_message, font=('Arial Bold', 10))
lbl0.place(x=30, y=80)

lbl2 = Label(window, text='Username')
lbl2.place(x=25, y=105)
user= Entry(window, width=20)
user.place(x=150, y=105)

lbl3 = Label(window, text='Password')
lbl3.place(x=25, y=125)
pwd = Entry(window, width=20)
pwd.place(x=150, y=125)

lbl4 = Label(window, text='Host')
lbl4.place(x=25, y=145)
host = Entry(window, width=20)
host.place(x=150, y=145)

lbl5 = Label(window, text='Auth Source')
lbl5.place(x=25, y=165)
auth = Entry(window, width=20)
auth.place(x=150, y=165)

lbl5 = Label(window, text='Port')
lbl5.place(x=25, y=185)
port = Entry(window, width=20)
port.place(x=150, y=185)

lbl6 = Label(window, text='Database name')
lbl6.place(x=25, y=205)
dbname = Entry(window, width=20)
dbname.place(x=150, y=205)

#------------------Destination data--------------------

l2_message = 'Data to restore'
lbl0 = Label(window, text=l2_message, font=('Arial Bold', 10))


lbl7 = Label(window, text='Username')
user_dest = Entry(window, width=20)


lbl8 = Label(window, text='Password')
pwd_dest = Entry(window, width=20)


lbl9 = Label(window, text='Host')
host_dest = Entry(window, width=20)


lbl10 = Label(window, text='Auth Source')
Auth_dest = Entry(window, width=20)


lbl11 = Label(window, text='Port')
port_dest = Entry(window, width=20)


lbl12 = Label(window, text='Database name')
dbname_dest = Entry(window, width=20)

backup_name = Label(window, text='Backup name')
back_entry = Entry(window, width=20)
backup_name.place(x=320, y=165)
back_entry.place(x=440, y=165)


def clicked():
    # if len(user.get()) == 0 or len(pwd.get()) == 0 or len(host.get()) == 0 or \
    #         len(port.get()) == 0 or len(dbname.get()) == 0:
    #     messagebox.showinfo('Problem', 'Please insert all the data for the database you want to backup')
    if (len(host_dest.get()) == 0 or
            len(port_dest.get()) == 0 or len(dbname_dest.get()) == 0) and rest_check.get():
        messagebox.showinfo('Problem', 'Please insert all the data for the database you want to restore')
    else:
        list1 = {'source': {'username': user.get(), 'password': pwd.get(), 'host': host.get(), 'port': port.get(),
                            'dbname': dbname.get(), 'auth': auth.get()},
                 'destination': {'username': user_dest.get(), 'password': pwd_dest.get(), 'host': host_dest.get(),
                                 'port': port_dest.get(), 'dbname': dbname_dest.get(), 'auth': Auth_dest.get()},
                 'backup_name': back_entry.get()}

        if rest_check.get():
            return_code = backup_data(1, list1)
            restore_i(list1)
        else:
            return_code = backup_data(0, list1)
        if return_code == '9000':
            messagebox.showinfo('SUCCESS', 'Backup created')


btn = Button(window, text="Let's Get Started!", command=clicked)
btn.place(x=300, y=300)


def restore_dest():
    if rest_check.get():
        lbl0.place(x=320, y=80)
        lbl7.place(x=320, y=105)
        lbl8.place(x=320, y=125)
        user_dest.place(x=440, y=105)
        pwd_dest.place(x=440, y=125)
        dbname_dest.place(x=440, y=205)
        lbl9.place(x=320, y=145)
        host_dest.place(x=440, y=145)
        lbl10.place(x=320, y=165)
        Auth_dest.place(x=440, y=165)
        lbl11.place(x=320, y=185)
        port_dest.place(x=440, y=185)
        lbl12.place(x=320, y=205)
        backup_name.place(x=200, y=260)
        back_entry.place(x=300, y=260)
    else:
        lbl0.place_forget()
        lbl7.place_forget()
        lbl8.place_forget()
        user_dest.place_forget()
        pwd_dest.place_forget()
        dbname_dest.place_forget()
        lbl9.place_forget()
        host_dest.place_forget()
        lbl10.place_forget()
        Auth_dest.place_forget()
        lbl11.place_forget()
        port_dest.place_forget()
        lbl12.place_forget()
        backup_name.place(x=320, y=165)
        back_entry.place(x=440, y=165)


rest_check = tk.BooleanVar()
btn_chek = Checkbutton(window, text="restore database ?", command=restore_dest, variable=rest_check,
                       onvalue=True, offvalue=False)
btn_chek.place(x=150, y=300)

window.mainloop()


