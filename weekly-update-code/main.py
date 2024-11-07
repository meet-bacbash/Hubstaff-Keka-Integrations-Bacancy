from fetch_data import fetch_data
from keka_log import keka_log


filename = input("Enter filename : ")
user_id = input("Enter user id : ")

fetch_data(filename=filename)

keka_log(user_id=user_id)
