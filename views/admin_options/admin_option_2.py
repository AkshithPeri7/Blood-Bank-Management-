from tkinter import *
from utils import create_label, wipe_page
from __main__ import cursor, connection
from tkinter import messagebox

def table_data(frame, x):
    wipe_page(frame)

    records_f = "|{:^15}|{:^15}|\n"
    title_f = "+{:^15}+{:^15}+\n"

    data_label = Label(frame, bg='#FBFCF8', width=40, height=15, font=('Lucida Console', 15), bd=0)
    data_label.place(x=30, y=90, anchor=NW, bordermode='ignore')

    def update_text():
        cursor.execute('select * from BloodTable')
        rows = cursor.fetchall()
        infos = ""
        infos += title_f.format('-'*15, '-'*15)
        infos += records_f.format('Blood Type', 'Units')
        infos += title_f.format('-'*15, '-'*15)
        for row in rows:
            infos += records_f.format(row[0] + row[2], str(row[1]))

        infos += title_f.format('-'*15, '-'*15)
        data_label['text'] = infos
    
    update_text()

    create_label(frame, "* 1 Unit = 1 pint = 450 mL", 400, 400, font=('Josefins Sans', 14))