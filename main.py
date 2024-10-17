from persistqueue import Queue
from hubstaff_data import hubstaff_main
from queue_fetch import keka_main
import logging

logging.basicConfig(filename="hubstaff_logs.log", format='%(asctime)s : %(message)s', filemode='a')
logger = logging.getLogger("hubstaff_logger")
logger.setLevel(logging.INFO)

q1 = Queue("user_timings_queue", autosave=True)

hubstaff_main(q1)

logging.basicConfig(filename="keka_logs.log", format='%(asctime)s : %(message)s', filemode='a')
logger = logging.getLogger("hubstaff_logger")
logger.setLevel(logging.INFO)

keka_main(q1)