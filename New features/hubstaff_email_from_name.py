import csv
import json
import sqlite3

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

user_dict = {}

with open('Downloads/bacancy-technology-llp_time_and_activities_report_2024-11-01_to_2024-11-11.csv', mode ='r')as file:
    csv_reader = csv.DictReader(file)
    # Iterate over each row
    for row in csv_reader:
        name = row['Member']
        email = row['Work email']

        print(f"{name} : {email}")

        cursor.execute('''
        Update users set hubstaff_name = ? where email = ?
        ''', (name,email))

        connection.commit()
