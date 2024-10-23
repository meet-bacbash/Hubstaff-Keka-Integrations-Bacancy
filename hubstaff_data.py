import os
import sqlite3

import requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(override=True)
access_token = os.getenv('access_token')
bac_org_id = 422392
connection = sqlite3.connect('db.sqlite3')

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


def hubstaff_main(q1,logger):

    todays_date = date.today()
    yesterdays_date = todays_date - timedelta(days=1)

    start_date = f'{yesterdays_date}T00:00:00Z'
    end_date = f'{yesterdays_date}T23:59:00Z'

    # start_date = '2024-10-21T00:00:00Z'
    # end_date = '2024-10-21T23:59:00Z'

    url = f'https://api.hubstaff.com/v2/organizations/{bac_org_id}/activities'

    cursor = connection.cursor()

    query = "SELECT keka_id,hubstaff_id FROM users where status = 1"
    cursor.execute(query)

    rows = cursor.fetchall()

    user_ids = {row[0]: row[1] for row in rows}

    with tqdm(total=len(user_ids), desc="Fetching Data", unit="chunk") as pbar:
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
                # print(data)

                if data['activities']:
                    # created_at_times = [gmt_to_ist(activity['created_at']) for activity in data['activities'] if activity['created_at'].split("T")[0] in start_date ]
                    started_at_times = [activity for activity in data['activities']]
                    only_dates = [activity['starts_at'] for activity in data['activities']]

                    clock_in_time = min(only_dates)
                    max_date = max(only_dates)

                    for entry in started_at_times:
                        if entry['starts_at'] == max_date:
                            date_obj = datetime.strptime(entry['starts_at'], "%Y-%m-%dT%H:%M:%Sz")
                            clock_out_time = date_obj + timedelta(seconds=int(entry['tracked']))
                            clock_out_time = clock_out_time.strftime("%Y-%m-%dT%H:%M:%Sz")

                    clock_in_time = gmt_to_ist(clock_in_time)
                    clock_out_time = gmt_to_ist(clock_out_time)


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

                    logger.info(f"{response.status_code} : user - {user_values}")
                else:
                    logger.error(f"User activities not found : user - {key}")

            else:
                print(f"Error: {response.status_code}, {response.text}")
                logger.error(f"{response.status_code} - {response.text}")

            pbar.update(1)

    return "Fetching data from hubstaff"

def hubstaff_id_sync():
    """

    :return:
    """

    url = f'https://api.hubstaff.com/v2/organizations/{bac_org_id}/members'

    # Headers with the PAT
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }


    cursor = connection.cursor()

    query = "SELECT id, email FROM users where status = 0"
    cursor.execute(query)

    row = cursor.fetchall()

    for i in row:
        params = {
            "search[email]": i[1]
        }

        response = requests.get(url, headers=headers, params=params)

        # Check the response
        if response.status_code == 200:
            users = response.json()
            if users['members'] != []:
                hubstaff_id = users['members'][0]['user_id']
                print(hubstaff_id)
                query = ""
                cursor.execute('''
                Update users set hubstaff_id = ?, status = 1 where id = ?
                ''',(hubstaff_id, i[0]))

                connection.commit()

            else:
                print(f"{i[1]}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

hubstaff_id_sync()