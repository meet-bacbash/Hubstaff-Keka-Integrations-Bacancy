import requests

def keka_main(q1, logger):

    l1 = []
    url = "https://cin02.a.keka.com/v1/logs"

    while not q1.empty():
        l1.append(q1.get())

    for i in l1:
        val = [{
            "DeviceIdentifier": "648f6f6a-1edb-42fa-9f4a-3afaf254afdd",
            "EmployeeAttendanceNumber": i['keka_id'],
            "Timestamp": i['clock_in_time'],
            "Status": 0
        }
        ,{
            "DeviceIdentifier": "648f6f6a-1edb-42fa-9f4a-3afaf254afdd",
            "EmployeeAttendanceNumber": i['keka_id'],
            "Timestamp": i['clock_out_time'],
            "Status": 1
        }]

        payload = f"""
        [
            {', '.join([f'''
            {{
                "DeviceIdentifier": "{entry['DeviceIdentifier']}",
                "EmployeeAttendanceNumber": "{entry['EmployeeAttendanceNumber']}",
                "Timestamp": "{entry['Timestamp']}",
                "Status": {entry['Status']}
            }}''' for entry in val])}
        ]
        """

        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': '29096d92-5808-4940-9ce0-f6ecbc305860'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            print(response.text)
            logger.info(f"{response.status_code} - {response.text} : payload - {payload}")
        else:
            logger.error(f"{response.status_code} - {response.text} : payload - {payload}")
            i['status_code'] = response.status_code
            i['status_text'] = response.text
            q1.put(i)
            print(f"Error: {response.status_code}, {response.text}")