import logging


def set_config():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(message)s',
        datefmt='%M:%S'
    )


class Logger:
    def __init__(self):
        set_config()

    def log(self, message):
        logging.info(message)

