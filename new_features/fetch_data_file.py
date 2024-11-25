"""
fetch_data_file will extract the employee logs from the file in downloads
"""
import csv
import sqlite3
from tqdm import tqdm

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()
user_dict = {}

def fetch_data(logger, q1, filename):
    """

    :param logger:
    :param q1:
    :param filename:
    :return updated queue:

    """

    with open(f'Downloads/{filename}', mode ='r', encoding="utf-8")as file:
        csv_reader = csv.DictReader(file)
        with tqdm(csv_reader,desc="Fetching Data from CSV file", unit="rows") as pbar:
            for row in csv_reader:
                if row:
                    name = row['Member']  # Assuming 'name' is the column with the names

                    cursor.execute('''
                    SELECT keka_id FROM users where hubstaff_name = ?
                    ''', (name,))

                    user_keka_id = cursor.fetchone()

                    if not user_keka_id:
                        logger.error(f"Keka id not found for hubstaff name : {name}")
                        continue

                    data = {"clock_in": row['Started'].split("+")[0], "clock_out": row['Stopped'].split("+")[0]}

                    # If the name already exists in the dictionary, append the row to the list
                    if user_keka_id[0] in user_dict:
                        user_dict[user_keka_id[0]].append(data)
                        logger.info(f"Keka Id : {user_dict[user_keka_id[0]]} : Details - {data}")
                    else:
                        # If the name doesn't exist, create a new list with the row
                        user_dict[user_keka_id[0]] = [data]
                        logger.info(f"Keka Id : {user_dict[user_keka_id[0]]} : Details - {data}")
                pbar.update(1)

    q1.put(user_dict)
