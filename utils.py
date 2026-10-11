import os

# --- Function to fetch relative path to a file
def pathLoad(path): 
    return './' + path


# -- Function to delete ALL Labels, images, entries, canvases
def wipe_page(source):
    from tkinter import Label

    # Get all widgets
    widget_list = list(source.winfo_children())
    for widget in widget_list:
        if isinstance(widget, Label) and widget['text'].startswith('|'):
            pass
        else: widget.destroy()

# -- Function to verify given pin code
def pinVerify(pin):
    if pin[0] == '0' or len(pin) != 6:
        return False
    elif int(pin[:2]) in [29, 35, 54, 55, 65, 66]:
        return False
    else: return True


# --- Custom function to create entries
def create_entry(control, x_position, y_position, text, **kwargs):
    from tkinter import Entry
    
    # Set default values for the appearance of the input field
    kwargs.setdefault('bd', 16)
    kwargs.setdefault('relief', 'flat')
    
    entry = Entry(control, **kwargs)
    entry.place(x=x_position, y=y_position)
    entry.insert(0, text)
    return entry


# --- Custom function to create buttons
def create_button(control, text, x_position, y_position, **kwargs):
    from tkinter import Button
    # kwargs is a dictionary containing all the option we used for Button()

    # Set default values for the appearance of the button
    defaults = {
        'activebackground': '#FF5733',
        'background': '#EE4B2B',
        'font': ('Century Gothic', 11),
        'bd': 0,
        'padx': 35,
        'pady': 10
    }
    for option, value in defaults.items():
        kwargs.setdefault(option, value)

    # Then create the button with all parameters
    button = Button(control, text=text, **kwargs)
    button.pack()
    button.place(x=x_position, y=y_position)
    return button


# --- Custom functions to create labels
def create_label(control, text, x_position, y_position, **kwargs):
    from tkinter import Label

    label = Label(control, text=text, **kwargs)
    label.pack()
    label.place(x=x_position, y=y_position)
    return label


# --- Preload all images and icons
def create_images():
    from tkinter import PhotoImage

    image_paths_dict = {
        0: 'backgrounds/bg-blurred.png',      1: 'backgrounds/bg-login.png',
        2: 'backgrounds/button-login.png',    3: 'backgrounds/profile-page.png',
        4: 'backgrounds/admin_welcome.png',
        
        5: 'icons/logo-80.png',  6: 'icons/icon.png',   7: 'icons/profile.png',
        8: 'icons/lg.png',       9: 'icons/menu.png',   10: 'icons/home.png'
    }

    for index, path in image_paths_dict.items():
        image_paths_dict[index] = PhotoImage(file=pathLoad('resources/' + path))
    
    return image_paths_dict
