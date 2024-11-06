import csv
import sqlite3
from persistqueue import Queue
from datetime import datetime


connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

q1 = Queue("user_timings_queue", autosave=True)
user_dict = {}

with open('data/data.csv', mode ='r')as file:
    csv_reader = csv.DictReader(file)
    # Iterate over each row
    for row in csv_reader:
        if row:
            start = row['Started']
            stop = row['Stopped']

            dt_obj = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")

            date = dt_obj.date()
            date_str = date.strftime("%Y-%m-%d")

            data = {"clock_in": row['Started'].split("+")[0], "clock_out": row['Stopped'].split("+")[0]}

            if date_str in user_dict:
                user_dict[date_str].append(data)
            else:
                user_dict[date_str] = [data]

q1.put(user_dict)
