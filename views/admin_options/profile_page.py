from tkinter import *
from utils import create_button, create_entry, pinVerify
from __main__ import cursor, connection

#               ------------------- Preliminary Functions ----------------------              

text_style  = {"font":('Josefin Sans', 27), "fill":"white", "anchor": "nw"}

def load_page(root, images, data):
    global topRoot, globalImages, admin
    topRoot = Toplevel(root)
    topRoot.iconphoto(False, images[6])
    topRoot.protocol('WM_DELETE_WINDOW', DEL_EVENT)
    topRoot.resizable(False, False)

    globalImages = images
    admin = data

    sub_profile_view()

#               ------------------ Page Handling Functions ----------------------              

def sub_profile_view():
    global topRoot, globalImages, admin, profCanvas

    # Make widget and info text
    profCanvas = Canvas(topRoot, width=500, height=400, highlightthickness=0)
    profCanvas.pack(fill=BOTH)
    profCanvas.create_image(0, 0, image=globalImages[3], anchor=NW)
    profCanvas.create_image(53, 53, image=globalImages[7], anchor=NW)

    profCanvas.create_text(60, 90, text=f'{admin["Name"].title()}', **text_style )
    profCanvas.create_text(60, 130, text=f'Reg. ID: ' + f'{admin["ID"]}'.zfill(4), **text_style )
    Pin = profCanvas.create_text(60, 170, text=f'Pin Code: {admin["Pin"]}', **text_style )

    # Define states to manage widget visibility
    EDITING_STATE = "editing"
    DEFAULT_STATE = "default"

    current_state = DEFAULT_STATE

    def set_state(state):
        nonlocal current_state
        current_state = state
        update_widget_visibility()

    def update_widget_visibility():
        if current_state == DEFAULT_STATE:
            pinEntry.place(x=-200, y=-180)
            editBtn.place(x=60, y=300)
            editBtn_stop.place(x=-50, y=-50)
            editBtn_save.place(x=-50, y=-50)
        elif current_state == EDITING_STATE:
            pinEntry.place(x=200, y=180)
            editBtn.place(x=-50, y=-50)
            editBtn_stop.place(x=60, y=300)
            editBtn_save.place(x=240, y=300)

    def edit_profile():
        set_state(EDITING_STATE)

    def stop_profile_edit():
        set_state(DEFAULT_STATE)

    def save_profile_edit():
        query = "update hospital set PinCode=%s where HospitalName=%s"
        pinVal = pinEntry.get()

        if pinVerify(pinVal):
            values = (pinVal, admin["Name"])
            cursor.execute(query, values)
            connection.commit()

            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pinVal}')
            admin["Pin"] = int(pinVal)
        else: return

        stop_profile_edit()

    pinEntry = create_entry(topRoot, -200, -180, '')
    editBtn = create_button(topRoot, 'Edit Pin Code', 60, 300, command=lambda: edit_profile())
    editBtn_stop = create_button(topRoot, 'Stop Editing', 60, 300, command=lambda: stop_profile_edit())
    editBtn_save = create_button(topRoot, 'Save Pin Code', 60, 300, command=lambda: save_profile_edit())

    update_widget_visibility()


# A function to make profile window invisible
def DEL_EVENT():
    global topRoot
    topRoot.destroy()