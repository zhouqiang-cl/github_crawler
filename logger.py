# -*- coding=utf-8-*-

import logging
import os
import tornado.log
from tornado.log import access_log, app_log, gen_log

import settings


if not os.path.exists(settings.LOG_PATH):
    os.makedirs(settings.LOG_PATH)


gen_handler = logging.FileHandler(settings.LOG_PATH + '/gen.log')

formatter = tornado.log.LogFormatter(fmt='%(color)s[ %(asctime)s %(module)s %(filename)s %(funcName)s %(module)s:%(lineno)d]%(end_color)s %(message)s',
                                     datefmt='%y/%m/%d %H:%M:%S')
gen_handler.setFormatter(formatter)

gen_log.addHandler(gen_handler)

gen_log.setLevel(logging.INFO)

