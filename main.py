from persistqueue import Queue
import logging

from token_validator import token_validator, get_access_token

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

# logging.basicConfig(filename="hubstaff_logs.log", format='%(asctime)s : %(message)s', filemode='a')
# logger = logging.getLogger("hubstaff_logger")
# logger.setLevel(logging.INFO)

get_access_token()

q1 = Queue("user_timings_queue", autosave=True)

logger1 = setup_logger('hubstaff_logger', 'hubstaff_logs.log')

from hubstaff_data import hubstaff_main
hubstaff_main(q1, logger1)

logger2 = setup_logger('keka_logger', 'keka_logs.log')

from queue_fetch import keka_main
keka_main(q1, logger2)