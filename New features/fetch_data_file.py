import csv
import json
import sqlite3
from persistqueue import Queue

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

q1 = Queue("user_timings_queue", autosave=True)
user_dict = {}

with open('Downloads/bacancy-technology-llp_work_sessions_report_2024-10-22_to_2024-10-22.csv', mode ='r')as file:
    csv_reader = csv.DictReader(file)
    # Iterate over each row
    for row in csv_reader:
        name = row['Member']  # Assuming 'name' is the column with the names

        # cursor.execute('''
        # SELECT keka_id FROM users where name = ?
        # ''', (name,))
        #
        # rows = cursor.fetchone()
        #
        # breakpoint()

        data = {"name":row['Member'],"clock_in": row['Started'].split("+")[0], "clock_out": row['Stopped'].split("+")[0]}

        # q1.put(data)

        # If the name already exists in the dictionary, append the row to the list
        if name in user_dict:
            user_dict[name].append(data)
        else:
            # If the name doesn't exist, create a new list with the row
            user_dict[name] = [data]

with open('user_data.json', 'w') as f:
    json.dump(user_dict, f, indent=4)