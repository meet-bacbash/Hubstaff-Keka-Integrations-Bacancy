import os
import requests
import dotenv
from dotenv import load_dotenv
from sqlalchemy import false

from app.extensions.db import db
from app.hubstaff.get_hubstaff_token import get_access_token


bac_org_id = 422392

def hubstaff_id_sync(email):
    """

    :return:
    """
    # dotenv
    dotenv_file = dotenv.find_dotenv()
    load_dotenv()

    url = f'https://api.hubstaff.com/v2/organizations/{bac_org_id}/members'

    # Headers with the PAT
    headers = {
        'Authorization': f"Bearer {os.getenv('access_token')}",
        'Content-Type': 'application/json'
    }

    params = {
        "search[email]": email
    }

    response = requests.get(url, headers=headers, params=params)

    # Check the response
    if response.status_code == 200:
        users = response.json()
        if users['members'] != []:
            hubstaff_id = users['members'][0]['user_id']
            print(hubstaff_id)
            return hubstaff_id
        else:
            print(f"Hubstaff account not found for {email}")
            return 0
    elif response.status_code == 401 and response.json()['error'] == "invalid_token":
        print("Invalid token")
        os.environ['access_token'] = get_access_token()
        return hubstaff_id_sync(email)
    else:
        print("Error fetching hubstaff account")
