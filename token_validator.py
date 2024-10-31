import os
import requests
import dotenv
from dotenv import load_dotenv

# dotenv
dotenv_file = dotenv.find_dotenv()
load_dotenv()

access_token = os.getenv('access_token')
bacancy_pat_token = os.getenv('bacancy_pat_token')

def get_access_token():
    """
    It will be used to get the access token for the hubstaff account from PAT
    :return: access token and new refresh token
    """
    # Token endpoint URL
    token_url = 'https://account.hubstaff.com/access_tokens'

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': bacancy_pat_token
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_response = response.json()
        new_access_token = token_response.get('access_token')
        new_refresh_token = token_response.get('refresh_token')  # If the refresh token is rotated
        dotenv.set_key(dotenv_file, "access_token", new_access_token)
        dotenv.set_key(dotenv_file, "refresh_token", new_refresh_token)
        print(f"New Access Token generated")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def token_validator():

    url = f'https://api.hubstaff.com/v2/users/me'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # users = response.json()
        print("Token validation Successful")
    elif response.status_code == 401 and response.json()['error'] == "invalid_token":
        get_access_token()
    else:
        print(f"Error: {response.status_code}, {response.text}")


    # Error: 401, {"error":"invalid_token","error_description":"The access token provided is expired, revoked, malformed or invalid for other reasons."}