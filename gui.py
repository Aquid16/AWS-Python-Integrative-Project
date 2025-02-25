from tkinter import *
from tkinter import ttk
#import sys
import os

def open_ec2_window():
    ec2_management_window = Toplevel(main_window)

    ec2_management_window.title("EC2 Management Window")
    ec2_frm = ttk.Frame(ec2_management_window, padding=10)
    ec2_frm.grid()

    Label(ec2_frm, text="EC2 Management Window").grid(column=0, row=0)

    btn = Button(ec2_frm, text="Create Instance")

    btn.bind("<Button>", lambda e: ec2_creation(ec2_frm))

    btn.grid(column=0, row=1)

def create_instance(ins_type, ins_os, ins_name, ins_amount):
    print(ins_amount)
    os.system(f'python manage.py create-instance --type {ins_type} --os {ins_os}'
              f' --name {ins_name} --amount {ins_amount}')
    #os.system('python manage.py create-instance --type t3.nano --os ubuntu --name sharon --amount 1')

def ec2_creation(ec2_frm):

    for widget in ec2_frm.winfo_children():
        widget.destroy()

    inst_type_options = ["None", "t3.nano", "t4g.nano"]
    inst_os_options = ["None", "ubuntu", "amazon-linux"]
    inst_amount_options = [0, 1, 2]

    inst_type_clicked = StringVar()
    inst_os_clicked = StringVar()
    inst_name_entered = StringVar()
    inst_amount_clicked = IntVar()

    label = ttk.Label(ec2_frm, text="EC2 Management")
    type_text = ttk.Label(ec2_frm, text="Type:")
    option_menu1 = ttk.OptionMenu(ec2_frm, inst_type_clicked, *inst_type_options)
    os_text = ttk.Label(ec2_frm, text="OS:")
    option_menu2 = ttk.OptionMenu(ec2_frm, inst_os_clicked, *inst_os_options)
    name_text = ttk.Label(ec2_frm, text="Instance Name:")
    entry = ttk.Entry(ec2_frm, textvariable=inst_name_entered)
    amount_text = ttk.Label(ec2_frm, text="Amount:")
    option_menu3 = ttk.OptionMenu(ec2_frm, inst_amount_clicked, *inst_amount_options)
    btn = ttk.Button(ec2_frm, text="Create",
               command=lambda: create_instance(inst_type_clicked.get(), inst_os_clicked.get(),
                                               inst_name_entered.get(),
                                               inst_amount_clicked.get()))

    label.grid(columnspan=2)
    type_text.grid(column=0, row=1)
    option_menu1.grid(column=1, row=1)
    os_text.grid(column=0, row=2)
    option_menu2.grid(column=1, row=2)
    name_text.grid(column=0, row=4)
    entry.grid(column=1, row=4)
    amount_text.grid(column=0, row=3)
    option_menu3.grid(column=1, row=3)
    btn.grid(columnspan=2)

# Main Window
main_window = Tk()
main_window.title("AWS Management Tool")
main_window.configure(background='black')

main_frm = ttk.Frame(main_window, padding=100)
main_frm.grid()
ttk.Label(main_frm, text="AWS Management Tool").grid(column=0, row=0)
ttk.Button(main_frm, text="EC2 Management", command=open_ec2_window).grid(column=0, row=1)

main_window.mainloop()