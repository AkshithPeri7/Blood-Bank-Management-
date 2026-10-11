import mysql.connector as sql
from tkinter import messagebox
from utils import pathLoad

def create_tables():
    #    MySQL password
    MYSQL_PASSWORD = "root"

    try:
        connection = sql.connect(
            host='localhost', user='root', password=MYSQL_PASSWORD)
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'MYSQL failed to start')
        exit()


    #    Check whether "bloodbank_2023_24" database exists and use it
    cursor.execute('create database if not exists bloodbank_2023_24')
    cursor.execute('use bloodbank_2023_24')

    #    Fetch all tables...
    cursor.execute('show tables')

    #    ...IF there are 0 tables in the database, create the tables
    if len(cursor.fetchall()) == 0:
        with open('./resources/commands.sql') as fp:
            for statement in fp.readlines():
                if statement.startswith('create') or statement.startswith('insert'):
                    print(statement)
                    cursor.execute(statement.strip())

    # Save changes
    connection.commit()

    return connection, cursor
