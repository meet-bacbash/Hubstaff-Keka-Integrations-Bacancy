import sqlite3
import pandas as pd

connection = sqlite3.connect('db.sqlite3')

def table_creation():
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_details (
        id INTEGER PRIMARY KEY,
        count_value INTEGER
    )
    ''')

    # Step 4: Commit the changes
    connection.commit()

    connection.close()

    print("Database created successfully!")

def emp_entry():

    df = pd.read_excel("remote_employee_list.xlsx")

    cursor = connection.cursor()

    for index, row in df.iterrows():
        keka_id = int(row['Emp ID'])
        emp_name = row['Employee Name'].replace('\n', '')
        emp_email = row['Email ID ']
        print("start")
        print(keka_id)
        print(emp_email)
        print(emp_name)
        print("end")

        cursor.execute('''
        INSERT INTO users("name","email","keka_id")
        VALUES (?,?,?);''',(emp_name,emp_email, keka_id))

        connection.commit()

    connection.close()
    print("Users created successfully!")
emp_entry()