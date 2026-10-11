from tkinter import Canvas, messagebox
from __main__ import connection, cursor
from utils import create_button, create_entry, create_images, wipe_page

# --------------------------- Handle login function for admin page ----------------------------

globalImages = create_images()

#               ------------------- Preliminary Functions ----------------------              

def setText(entry, defaultText):
    if entry.get().strip() == defaultText:
        entry.delete(0, "end")

def restoreText(entry, defaultText):
    if entry.get().strip() == "":
        entry.insert(0, defaultText)

def custom_entry(control, x, y, text):
    entry = create_entry(control, x, y, text, width=70)
    entry.bind('<FocusIn>', lambda event: setText(entry, text))
    entry.bind('<FocusOut>', lambda event: restoreText(entry, text))
    return entry

#               ------------------ Page Handling Functions ----------------------              

def make_canvas(control):
    canvas = Canvas(control, width='940', height='500', highlightthickness=0)
    # Add Background
    canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
    canvas.pack(side="top", fill="both", expand=True)
    return canvas


def validate_cred(control, admin_user, admin_pass):
    admin_user, admin_pass = admin_user.strip(), admin_pass.strip()

    if (admin_user == 'User Name' or admin_pass == 'Password' or
            len(admin_user) == 0 or len(admin_pass) == 0 or
            admin_user.isdigit() or admin_pass.isdigit()):
        messagebox.showerror('Error', 'Invalid login details')
        return

    cursor.execute(f"SELECT * FROM hospital WHERE HospitalName='{admin_user}' AND Password='{admin_pass}'")
    info = cursor.fetchone()

    if info is None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return

    hospital_ID, pincode = info[0], info[4]
    wipe_page(control)

    from views.admin_page import admin_login
    admin_login(admin_user, admin_pass, hospital_ID, pincode, control)



#               ----------------------- Login Page Code ----------------------              

def admin_login(root):
    login_canvas = make_canvas(root)

    # Text on the page
    label_look = {"anchor": "nw", "fill":"white"}
    login_canvas.create_text(355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), **label_look)
    login_canvas.create_text(470, 46, text='Login', font=('Josefin Sans', 25), **label_look)

    login_canvas.create_text(240, 180, text='Sign In', font=('Franklin Gothic', 16, 'bold'), **label_look)
    login_canvas.create_text(240, 200, text='Fill in details to gain access', font=('Josefin Sans', 14), **label_look)

    # Input 1
    user_name = custom_entry(root, 240, 260, 'Hospital Name')
    # Input 2
    user_pass = custom_entry(root, 240, 320, 'Password')
    # Login Button
    from views.welcome_page import welcome_screen
    create_button(root, 'Login', 345, 380, command= lambda: validate_cred(root, user_name.get(), user_pass.get()))
    create_button(root, 'Back', 465, 380, command= lambda: (wipe_page(root), welcome_screen(root)))

    