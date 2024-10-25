import csv
import json
import sqlite3
from persistqueue import Queue

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

q1 = Queue("user_timings_queue", autosave=True)
user_dict = {}

with open('Downloads/bacancy-technology-llp_work_sessions_report_2024-10-24_to_2024-10-24.csv', mode ='r')as file:
    csv_reader = csv.DictReader(file)
    # Iterate over each row
    for row in csv_reader:
        if row:
            name = row['Member']  # Assuming 'name' is the column with the names

            cursor.execute('''
            SELECT keka_id FROM users where hubstaff_name = ?
            ''', (name,))

            user_keka_id = cursor.fetchone()

            if not user_keka_id:
                continue


            data = {"clock_in": row['Started'].split("+")[0], "clock_out": row['Stopped'].split("+")[0]}

            # q1.put(data)

            # If the name already exists in the dictionary, append the row to the list
            if user_keka_id[0] in user_dict:
                user_dict[user_keka_id[0]].append(data)
            else:
                # If the name doesn't exist, create a new list with the row
                user_dict[user_keka_id[0]] = [data]

q1.put(user_dict)
