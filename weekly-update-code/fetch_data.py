import csv
import sqlite3
from persistqueue import Queue
from datetime import datetime


connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

q1 = Queue("user_timings_queue", autosave=True)
user_dict = {}

def fetch_data(filename):
    with open(f'data/{filename}.csv', mode ='r')as file:
        csv_reader = csv.DictReader(file)
        # Iterate over each row
        for row in csv_reader:
            if row:
                start = row['Started']

                dt_obj = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z").date()

                date_str = dt_obj.strftime("%Y-%m-%d")

                data = {"clock_in": row['Started'].split("+")[0], "clock_out": row['Stopped'].split("+")[0]}

                if date_str in user_dict:
                    user_dict[date_str].append(data)
                else:
                    user_dict[date_str] = [data]

    q1.put(user_dict)
