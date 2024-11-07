from email_file_fetch import download_attachments
from fetch_data_file import fetch_data
from keka_logs import keka_main

print("Downloading the latest file...")
download_attachments()
fetch_data()
keka_main()