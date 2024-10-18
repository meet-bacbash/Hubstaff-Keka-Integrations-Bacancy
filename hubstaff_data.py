import os
import sqlite3
import requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import dotenv

def gmt_to_ist(gmt_time_str):
    """
    Function to convert GMT to IST
    :param gmt_time_str:
    :return: ist time
    """
    try:
        # Parse the GMT datetime string
        gmt_time = datetime.strptime(gmt_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Convert to IST (GMT +5:30)
        gmt_time = gmt_time.replace(microsecond=0)
    except ValueError:
        # Parse the GMT datetime string
        gmt_time = datetime.strptime(gmt_time_str, '%Y-%m-%dT%H:%M:%SZ')
        # Convert to IST (GMT +5:30)
    ist_time = gmt_time + timedelta(hours=5, minutes=30)
    ist_time = ist_time.strftime("%Y-%m-%dT%H:%M:%S")
    return ist_time


def hubstaff_main(q1, logger):
    # Logging

    # dotenv
    dotenv_file = dotenv.find_dotenv()
    load_dotenv()

    access_token = os.getenv('access_token')
    bacancy_pat_token = os.getenv('bacancy_pat_token')

    todays_date = date.today()

    bac_org_id = 422392

    # start_date = f'{todays_date}T00:00:00Z'
    # end_date = f'{todays_date}T23:59:00Z'

    start_date = '2024-10-17T00:00:00Z'
    end_date = '2024-10-17T23:59:00Z'

    url = f'https://api.hubstaff.com/v2/organizations/{bac_org_id}/activities'

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    query = "SELECT keka_id,hubstaff_id FROM users"
    cursor.execute(query)

    # Step 4: Fetch the results
    rows = cursor.fetchall()

    # Step 5: Process the results
    user_ids = {row[0]: row[1] for row in rows}

    for key,value in user_ids.items():
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        params = {
            'time_slot[start]': start_date,
            'time_slot[stop]': end_date,
            'user_ids': value
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            users = response.json()
            data = users

            # Extract all 'created_at' values and convert them to IST
            created_at_times = [gmt_to_ist(activity['created_at']) for activity in data['activities']]
            started_at_times = [gmt_to_ist(activity['starts_at']) for activity in data['activities']]

            # Find the first and last created_at times
            clock_in_time = min(started_at_times)
            clock_out_time = max(created_at_times)

            query = "SELECT count_value FROM queue_count"
            cursor.execute(query)

            # Step 4: Fetch the results
            row = cursor.fetchall()

            user_values = {
                'id': row[0][0],
                'keka_id': key,
                'clock_in_time': clock_in_time,
                'clock_out_time': clock_out_time,
            }

            query = """
            UPDATE queue_count
            SET count_value = count_value + 1
            WHERE id = 1
            """
            cursor.execute(query)

            connection.commit()

            q1.put(user_values)

            # Print the results
            # print("First date (IST):", first_date)
            # print("Last date (IST):", last_date)
            logger.info(f"{response.status_code} : user - {user_values}")

        else:
            print(f"Error: {response.status_code}, {response.text}")
            logger.error(f"{response.status_code} - {response.text}")

    return "Fetching data from hubstaff"
