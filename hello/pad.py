import os.path
import random
import logging

import sys

logger = logging.getLogger('cdfgj')
# hdlr = logging.FileHandler('D:/userdata/owu/Desktop/cdfgj.log')
hdlr = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

max = 5

if __name__ == '__main__':
    i = 0
    while i < max and os.path.isfile("D:\owu\PycharmProjects\hellopython\hello\pad.py"):
        i += 1
        r = 20 + random.randint(1, 10)
        logger.info('exist and #%s' % r)
