from tkinter import Tk, messagebox, PhotoImage
from utils import pathLoad
import mysql.connector as sql

# Main Entry File
#     Stores the tkinter instance (root)
root = Tk()
root.withdraw()

#     and intialises its basic features
root.title('Blood Bank System')
root.iconphoto(False, PhotoImage(file='./resources/icons/icon.png'))
root.resizable(False, False)

#     also, sets the position of window on the screen
x_coordinate = (root.winfo_screenwidth() - 940) // 2
y_coordinate = (root.winfo_screenheight() - 500) // 2
root.geometry(f"940x500+{x_coordinate}+{y_coordinate}")

#    then initialise SQL
from sql_init import create_tables
connection, cursor = create_tables()

root.deiconify()
#    finally, start the program
if __name__ == "__main__":
    from views.welcome_page import welcome_screen
    welcome_screen(root)

    root.mainloop()
