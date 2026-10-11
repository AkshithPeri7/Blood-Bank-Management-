from tkinter import *
from tkinter import messagebox
from __main__ import connection, cursor
from utils import create_images, create_entry, create_button, create_label, wipe_page


# ----------------------------------- Admin Menu Handling -------------------------------------

from random import randint
images = create_images()

#               ------------------- Preliminary Functions ----------------------              

def donation_choice(src, ID, heading):
    global Admin_ID
    Admin_ID = ID
    wipe_page(src)

    create_label(src, 'Arrange donation for a person:', 40, 90, font=('Cascadia Code', 19))
    create_label(src, 'Transfer blood to another hospital:', 40, 240, font=('Cascadia Code', 19))

    create_button(src, 'Donate', 110, 150, command=lambda: (wipe_page(src), donate_blood_citizen(src, heading)),
            bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", padx=141, pady=8, fg='white', font=('Cascadia Code', 15))
    create_button(src, 'Transfer', 110, 300, command=lambda: (wipe_page(src), donate_blood_hospital(src, heading)),
            bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", padx=130, pady=8, fg='white', font=('Cascadia Code', 15))


# -------------------------------- Option Selection Handling ----------------------------------
#                --------------------- Option choice: 1 ----------------------              

def donate_blood_citizen(src, header):
    header['text'] = '|    Arranging Appointment'

    def make_lbl_entry(ctrl, text, x1, y1, x2, y2, w):
        nm = create_entry(src, x1, y1, '', width=w)
        lbl = create_label(src, text, x2, y2, font=('Josefin Sans', 18))
        return nm
    
    e_1 = make_lbl_entry(src, 'Enter name of person:', 270, 100, 40, 100, 60)
    e_2 = make_lbl_entry(src, 'Gender:', 130, 165, 40, 165, 9)
    e_3 = make_lbl_entry(src, 'Age:', 310, 165, 245, 165, 9)
    e_4 = make_lbl_entry(src, 'Blood Group Required:', 270, 240, 40, 240, 9)

    create_button(src, 'Appoint', 60, 340, command=lambda: validate())

    def validate():
        for i in [e_1.get(), e_2.get(), e_4.get()]:
            if i.isdigit() or len(i) == 0 or i.isspace():
                messagebox.showerror('Error', 'Failed to appoint user; Verify user details'); return

        if e_2.get().lower() not in ['male', 'female', 'm', 'f']: messagebox.showerror('Error', 'Enter a proper gender (M or F)'); return
        elif not e_3.get().isdigit(): messagebox.showerror('Error', 'Enter a valid age'); return
        elif int(e_3.get()) > 100: messagebox.showerror('Error', 'Enter a valid age'); return
        elif e_4.get().lower()[:-1] not in ['a', 'b', 'o', 'ab'] or e_4.get()[-1] not in ['-', '+']: messagebox.showerror('Error', 'Enter a valid Bloodtype'); return

        cursor.execute(f"SELECT COUNT(*) FROM recipient WHERE Name='{e_1.get()}'")
        if cursor.fetchone()[0] == 0:
            cursor.execute(f"insert into recipient values ({randint(1000, 9999)}, '{e_1.get()}', '{e_3.get()}', '{e_2.get()}', '{e_4.get()}', 0)")
        else:
            cursor.execute(f"update recipient set Donations=Donations + 1 where Name='{e_1.get()}'")
        connection.commit()

        messagebox.showinfo('Success', f'Successfully set up donation request for {e_1.get()}! Required: {e_4.get().upper()}')
        donation_choice(src, Admin_ID, header)


#                --------------------- Option choice: 2 ----------------------              

def donate_blood_hospital(src, header):
    global Admin_ID
    header['text'] = '|    Transferring Blood'
    create_label(src, 'Select the following;', 30, 100, font=('Josefin Sans', 18))


    # ---- For Hospital Dropdown
    create_label(src, 'Choose a hospital:', 40, 170, font=('Josefin Sans', 18))
    hosp_options, hosp_sval = [], StringVar(value='None')

    cursor.execute(f'select HospitalName, HospitalID from Hospital where HospitalID != {Admin_ID}')
    data = cursor.fetchall()
    if data != None:
        for row in data:
            hosp_options.append(row[0].title()) if row[1] != Admin_ID else None
    else:
        hosp_options.append('')
    hosp_menu = OptionMenu(src, hosp_sval, *hosp_options)
    hosp_menu.place(x=230, y=180)


    # ---- For label showcasing selected blood types
    global totalList, selected, display_label
    selected = []
    totalList = ""
    display_label = create_label(src, totalList, 550, 90, font=('Josefin Sans', 14), bg='#FBFCF8', padx=100, width=10, height=10, anchor='n')

    def option_selected(blood):
        global totalList, selected
        totalList += f"Requested: {blood}\n"
        selected.append(blood)
        display_label.config(text=totalList)

    def reset_selected():
        global selected, totalList
        selected.clear()
        totalList = ""
        display_label.config(text=totalList)


    # ---- For Blood Type(s) Dropdown
    create_label(src, 'Select Blood Type(s):', 40, 230, font=('Josefin Sans', 18))
    blood_options = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_sval = StringVar(value='        ')
    blood_menu = OptionMenu(src, blood_sval, *blood_options)
    blood_menu.place(x=260, y=240)

    blood_menu['menu'].delete(0, 'end')

    for option in blood_options:
        blood_menu['menu'].add_command(label=option, command=lambda v=option: option_selected(v))


    # ---- Buttons
    proceed = create_button(src, 'Proceed with donation', 40, 353, command=lambda: proceed_dono(src),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", font=('Cascadia Code', 10))

    reset = create_button(src, 'Reset Selections', 340, 353, command=lambda: reset_selected(),
        bd=0, activebackground='#D22B2B', bg='#EE4B2B', relief="flat", font=('Cascadia Code', 10))


    # ---- Function to validate the donation
    def proceed_dono(ctrl):
        global selected, Admin_ID

        if hosp_sval.get() == 'None' or len(selected) == 0:
            messagebox.showerror('Error', 'Select all options'); return

        for i in selected:
            cursor.execute('select Units from bloodtable where concat(BloodType, RhFactor) = "%s"'%(i,))

            # If Quantity of that blood type is 0, exit the loop
            if cursor.fetchone()[0] == 0: break

            query = f'update bloodtable set Units = Units - 1 where concat(BloodType, RhFactor) = "{i}"'
            cursor.execute(query)
        else:
            connection.commit()

            cursor.execute(f'select HospitalName, HospitalID from hospital where HospitalID = {Admin_ID}')
            data = cursor.fetchone()

            messagebox.showinfo('Success', f'Successfully donated {len(selected)} units of blood to {hosp_sval.get()}!')
            wipe_page(ctrl)
            donate_blood_hospital(ctrl, header)
            return

        # If for loop failed to execute
        messagebox.showerror('Error', 'Not enough storage of blood available')
        connection.rollback()
        return

# ---------------------------------------------------------------------------------------------
