import tkinter
import subprocess
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def open_ec2_window():
    ec2_management_window = Toplevel(main_window)

    ec2_management_window.title("EC2 Management Window")
    ec2_frm = ttk.Frame(ec2_management_window, padding=20)
    ec2_frm.grid()

    Label(ec2_frm, text="EC2 Management Window").grid(column=0, row=0)

    create_btn = Button(ec2_frm, text="Create Instance")
    list_btn = Button(ec2_frm, text="List Instances")
    manage_btn = Button(ec2_frm, text="Manage Instances")
    delete_btn = Button(ec2_frm, text="Delete Instance")

    create_btn.bind("<Button>", lambda e: ec2_creation(ec2_frm))
    list_btn.bind("<Button>", lambda e: ec2_listing(ec2_frm))
    manage_btn.bind("<Button>", lambda e: ec2_management(ec2_frm))
    delete_btn.bind("<Button>", lambda e: ec2_destruction(ec2_frm))

    create_btn.grid(column=0, row=1)
    list_btn.grid(column=0, row=2)
    manage_btn.grid(column=0, row=3)
    delete_btn.grid(column=0, row=4)

def open_s3_window():
    s3_management_window = Toplevel(main_window)

    s3_management_window.title("S3 Management Window")
    s3_frm = ttk.Frame(s3_management_window, padding=20)
    s3_frm.grid()

    Label(s3_frm, text="S3 Management Window").grid(column=0, row=0)

    create_btn = Button(s3_frm, text="Create Bucket")
    list_btn = Button(s3_frm, text="List Buckets")
    upload_btn = Button(s3_frm, text="Upload File")
    delete_btn = Button(s3_frm, text="Delete Bucket")

    create_btn.bind("<Button>", lambda e: s3_creation(s3_frm))
    list_btn.bind("<Button>", lambda e: s3_listing(s3_frm))
    upload_btn.bind("<Button>", lambda e: upload_to_s3(s3_frm))
    delete_btn.bind("<Button>", lambda e: s3_destruction(s3_frm))

    create_btn.grid(column=0, row=1)
    list_btn.grid(column=0, row=2)
    upload_btn.grid(column=0, row=3)
    delete_btn.grid(column=0, row=4)

def open_route53_window():
    return

def create_instance(ins_type, ins_os, ins_name, ins_amount):
    os.system(f'python manage.py create-instance --type {ins_type} --os {ins_os}'
              f' --name {ins_name} --amount {ins_amount}')

def destroy_instance(ins_id):
    os.system(f'python manage.py terminate-instance --instance-id {ins_id}')

def list_instances(text):
    try:
        result = subprocess.run(['python', 'manage.py', 'list-instances'], capture_output=True, text=True)

        if result.returncode == 0:
            instances = result.stdout.splitlines()

        text.delete(1.0, tkinter.END)

        for instance in instances:
            text.insert(tkinter.END, instance + "\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def start_instance(ins_id):
    os.system(f'python manage.py manage-instance --instance-id {ins_id} --operation start')

def stop_instance(ins_id):
    os.system(f'python manage.py manage-instance --instance-id {ins_id} --operation stop')

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

def ec2_listing(ec2_frm):
    for widget in ec2_frm.winfo_children():
        widget.destroy()

    label = ttk.Label(ec2_frm, text="EC2 Management")
    btn = ttk.Button(ec2_frm, text="List EC2 Instances", command= lambda: list_instances(output_text))
    output_text = tkinter.Text(ec2_frm, height=10, width=80)

    label.grid(columnspan=4)
    btn.grid(columnspan=4)
    output_text.grid(columnspan=4)

def ec2_management(ec2_frm):
    instance_ids = [""]

    for widget in ec2_frm.winfo_children():
        widget.destroy()

    try:
        result = subprocess.run(['python', 'manage.py', 'list-instances'], capture_output=True, text=True)

        if result.returncode == 0:
            instances = result.stdout.splitlines()

        for instance in instances:
            id_split = instance.translate(str.maketrans({':':' ', ',': ' '}))
            inst_id = id_split.split()
            instance_ids.append(inst_id[1])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    inst_id_clicked = StringVar()

    label = ttk.Label(ec2_frm, text="EC2 Management")
    id_text = ttk.Label(ec2_frm, text="ID:")
    option_menu = ttk.OptionMenu(ec2_frm, inst_id_clicked, *instance_ids)
    start_btn = ttk.Button(ec2_frm, text="Start Instance", command=lambda: start_instance(inst_id_clicked.get()))
    stop_btn = ttk.Button(ec2_frm, text="Stop Instance", command=lambda: stop_instance(inst_id_clicked.get()))

    label.grid(columnspan=2)
    id_text.grid(column=0, row=1)
    option_menu.grid(column=1, row=1)
    start_btn.grid(columnspan=2)
    stop_btn.grid(columnspan=2)

def ec2_destruction(ec2_frm):
    instance_ids = [""]

    for widget in ec2_frm.winfo_children():
        widget.destroy()

    try:
        result = subprocess.run(['python', 'manage.py', 'list-instances'], capture_output=True, text=True)

        if result.returncode == 0:
            instances = result.stdout.splitlines()

        for instance in instances:
            id_split = instance.translate(str.maketrans({':': ' ', ',': ' '}))
            inst_id = id_split.split()
            instance_ids.append(inst_id[1])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    inst_id_clicked = StringVar()

    label = ttk.Label(ec2_frm, text="EC2 Management")
    id_text = ttk.Label(ec2_frm, text="ID:")
    option_menu = ttk.OptionMenu(ec2_frm, inst_id_clicked, *instance_ids)
    btn = ttk.Button(ec2_frm, text="Delete", command= lambda: destroy_instance(inst_id_clicked.get()))

    label.grid(columnspan=2)
    id_text.grid(column=0, row=1)
    option_menu.grid(column=1, row=1)
    btn.grid(columnspan=2)

def create_bucket(name, access):
    try:
        command = ['python', 'manage.py', 'create-bucket', "--name", name, "--access", access]

        if access == "public":
            is_public = tkinter.messagebox.askyesno("S3 Bucket Visibility", "Are you sure you want to make the S3 bucket public?")

            if is_public:
                result = subprocess.run(command, input="yes", capture_output=True, text=True)

                if result.returncode == 0:
                    return result.stdout

                else:
                    return f"Error: {result.stderr}"

            else:
                return

        else:
            os.system(f'python manage.py create-bucket --name {name} --access {access}')

    except Exception as e:
        return f"An error occurred: {str(e)}"

def list_buckets(text):
    try:
        result = subprocess.run(['python', 'manage.py', 'list-buckets'], capture_output=True, text=True)

        if result.returncode == 0:
            buckets = result.stdout.splitlines()

        text.delete(1.0, tkinter.END)

        for bucket in buckets:
            text.insert(tkinter.END, bucket + "\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def destroy_bucket(name):
    os.system(f'python manage.py delete-bucket --name {name}')

def upload_file(file_path, name):
    os.system(f'python manage.py upload-file --path {file_path} --name {name} --key uploads/{browse()[1]}')

def browse():
    file = tkinter.filedialog.askopenfile(mode = "r",
                                          filetypes=[("All Files", ["*.*"])])
    if file:
        file_path = os.path.abspath(file.name)

    file_and_path = [file_path, file.name]
    return file_and_path

def s3_creation(s3_frm):
    for widget in s3_frm.winfo_children():
        widget.destroy()

    bucket_access_options = ["None", "private", "public"]

    bucket_access_clicked = StringVar()
    bucket_name_entered = StringVar()

    label = ttk.Label(s3_frm, text="S3 Management")
    name_text = ttk.Label(s3_frm, text="Bucket Name:")
    entry = ttk.Entry(s3_frm, textvariable=bucket_name_entered)
    access_text = ttk.Label(s3_frm, text="Access:")
    option_menu = ttk.OptionMenu(s3_frm, bucket_access_clicked, *bucket_access_options)
    btn = ttk.Button(s3_frm, text="Create", command=lambda: create_bucket(bucket_name_entered.get(),
                                                                          bucket_access_clicked.get()))

    label.grid(columnspan=2)
    name_text.grid(column=0, row=1)
    entry.grid(column=1, row=1)
    access_text.grid(column=0, row=2)
    option_menu.grid(column=1, row=2)
    btn.grid(columnspan=2)

def s3_listing(s3_frm):
    for widget in s3_frm.winfo_children():
        widget.destroy()

    label = ttk.Label(s3_frm, text="S3 Management")
    btn = ttk.Button(s3_frm, text="List S3 Buckets", command=lambda: list_buckets(output_text))
    output_text = tkinter.Text(s3_frm, height=10, width=80)

    label.grid(columnspan=4)
    btn.grid(columnspan=4)
    output_text.grid(columnspan=4)

def upload_to_s3(s3_frm):
    bucket_names = [""]

    for widget in s3_frm.winfo_children():
        widget.destroy()

    try:
        result = subprocess.run(['python', 'manage.py', 'list-buckets'], capture_output=True, text=True)

        if result.returncode == 0:
            buckets = result.stdout.splitlines()

        for bucket in buckets:
            bucket_names.append(bucket)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    bucket_name_clicked = StringVar()

    label = ttk.Label(s3_frm, text="S3 Management")
    name_text = ttk.Label(s3_frm, text="Bucket Name:")
    option_menu = ttk.OptionMenu(s3_frm, bucket_name_clicked, *bucket_names)
    file_path_entry_text = ttk.Label(s3_frm, text="File path:")
    file_path_entry = ttk.Entry(s3_frm)
    file_path_entry.delete(0, tkinter.END)
    file_path_entry.insert(0, browse()[0])
    upload_btn = ttk.Button(s3_frm, text="Upload File", command=lambda: upload_file(file_path_entry, bucket_name_clicked.get()))

    label.grid(columnspan=4)
    file_path_entry_text.grid(column=0, row=1)
    file_path_entry.grid(column=1, row=1)
    name_text.grid(column=0, row=2)
    option_menu.grid(column=1, row=2)
    upload_btn.grid(columnspan=4)

def s3_destruction(s3_frm):
    bucket_names = [""]

    for widget in s3_frm.winfo_children():
        widget.destroy()

    try:
        result = subprocess.run(['python', 'manage.py', 'list-buckets'], capture_output=True, text=True)

        if result.returncode == 0:
            buckets = result.stdout.splitlines()

        for bucket in buckets:
            bucket_names.append(bucket)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    bucket_name_clicked = StringVar()

    label = ttk.Label(s3_frm, text="S3 Management")
    name_text = ttk.Label(s3_frm, text="Bucket Name:")
    option_menu = ttk.OptionMenu(s3_frm, bucket_name_clicked, *bucket_names)
    print(bucket_name_clicked.get())
    btn = ttk.Button(s3_frm, text="Delete", command=lambda: destroy_bucket(bucket_name_clicked.get()))

    label.grid(columnspan=2)
    name_text.grid(column=0, row=1)
    option_menu.grid(column=1, row=1)
    btn.grid(columnspan=2)


# Main Window
main_window = Tk()
main_window.title("AWS Management Tool")
main_window.configure(background='black')

main_frm = ttk.Frame(main_window, padding=20)
main_frm.grid()
ttk.Label(main_frm, text="AWS Management Tool").grid(column=0, row=0)
ttk.Button(main_frm, text="EC2 Management", command=open_ec2_window).grid(column=0, row=1)
ttk.Button(main_frm, text="S3 Management", command=open_s3_window).grid(column=0, row=2)
ttk.Button(main_frm, text="Route53 Management", command=open_route53_window()).grid(column=0, row=3)

main_window.mainloop()