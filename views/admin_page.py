from tkinter import *
from utils import create_button, create_entry, create_images, create_label
from utils import pathLoad, pinVerify, wipe_page

# ----------------------------------- Admin Page Handling -------------------------------------

# Dictionary to hold admin information
admin_data = {"Name": None, "ID":None, "Pass":None, "Pin":None}
globalImages = create_images()
from views.admin_options.profile_page import load_page

#               ------------------- Preliminary Functions ----------------------              

def create_page(control):
    global scroll_texts, scrollbar, scrolling_started
    control.configure(bg='white')

    # Make the info crawl (top black bar)
    scroll_texts, scrolling_started = "", False
    scrollbar = create_label(control, "", 0, 0, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)


def crawl(txt):
    global scroll_texts, scrolling_started, scrollbar

    # Append new text to the scrolling content
    scroll_texts += txt

    # If scrolling content is too long, remove the oldest part
    if len(scroll_texts) > 140:
        scroll_texts = scroll_texts.split('  ', 7)[-1]

    scrollbar.config(text=scroll_texts)

    def rotate():
        global scroll_texts

        # Max number of characters in label is 187
        if len(scroll_texts) >= 187 + len(scroll_texts):
            scroll_texts = ""

        scroll_texts += "   "
        scrollbar.config(text=scroll_texts)
        scrollbar.after(100, rotate)

    if not scrolling_started:
        scrolling_started = True
        rotate()


def decorate(source):
    wipe_page(source)

    bg = Label(source, image=globalImages[4])
    bg.place(x=-2, y=-2)
    bg.lower()
    
    basic_Text = '\n|   App Guide:\n\n1.     ≡ is to navigate the menu\n2.     Profile button is to update hosptial details'
    create_label(source, basic_Text, -1, 230, width=140, bg='#FBFCF8', height=8, font=('Cascadia Code', 17), anchor=NW, justify=LEFT)

#                --------------------- Primary Functions ----------------------              

def load_admin_view(control):
    title_bar = Frame(control, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)

    button_look = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B", "image":globalImages[9]
    }

    # Add elements to the home bar at top (Hospital name, logo and button)
    menu_btn = Button(title_bar, **button_look, command= lambda: side_bar(control)).pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=globalImages[5]).pack(side=LEFT, padx=5)

    # Name of hospital label
    create_label(title_bar, admin_data["Name"].title(), 90, 0, fg="white", bg="#D22B2B",
        font=('Josefin Sans', 17), pady=0)
    # Profile Page Button
    create_button(title_bar, '', 830, 2, background='#D22B2B', activebackground='#D22B2B',
        image=globalImages[7], command= lambda: load_page(control, globalImages, admin_data))
    # Home Page button
    create_button(title_bar, '', 880, 2, background='#D22B2B', activebackground='#D22B2B',
        image=globalImages[10], command=lambda: decorate(display_frame))

    # Greet user
    global sidebar_opened
    sidebar_opened = False
    crawl(f'   Welcome {admin_data["Name"]}!   ')

    # Create window elements
    global current_view, display_frame

    display_frame = Frame(control, width=control.winfo_screenwidth(), height=440)
    display_frame.place(x=0, y=69)

    # Place images then place header
    decorate(display_frame)
    current_view = create_label(display_frame, '|    Hospital Management System', 0, 20, font=('Cascadia Code', 22), width=55, bg='#FBFCF8', height=1, anchor='w')


def side_bar(root):
    global home_bar, sidebar_opened, current_view, display_frame

    # Handling whether sidebar is open or not
    if sidebar_opened == True:
        home_bar.destroy()
        sidebar_opened = False
        return
    else:
        sidebar_opened = True

    home_bar = Frame(root, bg="#D22B2B", highlightthickness=2, highlightbackground='black')
    home_bar.pack(fill=Y)
    home_bar.place(relx=0, rely=0.138, relheight=1, relwidth=0.25)

    optionLooks = {
        "font": ("Corbel", 15), "padx":10, "relief": "flat", "fg": "white", "underline": 4,
        "activeforeground":"white", "background":"#D22B2B", "activebackground":"#D22B2B"
    }
    create_button(home_bar, '⦿    Donate/Recieve\nBlood', 16, 30, **optionLooks, command= lambda: menu_options(1))
    create_button(home_bar, '⦿    See Blood Bank', 16, 100, **optionLooks, command= lambda: menu_options(2))
    create_button(home_bar, 'EXIT', 10, 380, **optionLooks, command= lambda: menu_options(3))

    def dropFrame(txt):
        global sidebar_opened
        sidebar_opened = False; home_bar.destroy()
        crawl(txt)

    def menu_options(c):
        if c == 1:
            dropFrame('    Now Donating Blood    ')
            from views.admin_options.admin_option_1 import donation_choice
            donation_choice(display_frame, admin_data["ID"], current_view)
            current_view['text'] = '|    Choose an option'

        elif c == 2:
            dropFrame('    Now Managing Blood Storage    ')
            current_view['text'] = '|    Viewing Blood Storage'
            from views.admin_options.admin_option_2 import table_data
            table_data(display_frame, current_view)

        elif c == 3:
            wipe_page(root)
            from views.welcome_page import welcome_screen
            welcome_screen(root)


# -------------------------------- Main Page loader Function ----------------------------------

def admin_login(name, passw, ID, pin, control):
    admin_data["Name"] = name
    admin_data["Pass"] = passw
    admin_data["Pin"] = pin
    admin_data["ID"] = ID

    # First make the decorations
    create_page(control)

    # Then make the main frames
    load_admin_view(control)