"""
Program to fetch the latest employee report, fetch the details from file and add the logs to keka
"""

import logging
from persistqueue import Queue
from email_file_fetch import download_attachments

q1 = Queue("everyday_data_queue", autosave=True)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """
    Will help setup more than one logger
    :param name:
    :param log_file:
    :param level:
    :return:
    """
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


print("Downloading the latest file...")
filename = download_attachments()
print(f"Downloaded: {filename}")

if filename:
    from fetch_data_file import fetch_data
    logger1 = setup_logger('hubstaff_logger', 'hubstaff_logs.log')
    fetch_data(logger=logger1, q1=q1, filename=filename)

    from keka_logs import keka_main
    logger2 = setup_logger('keka_logger', 'keka_logs.log')
    keka_main(logger=logger2,q1=q1)
