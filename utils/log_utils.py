#! /usr/bin/python3
# -*- coding: UTF-8 -*-

"""Log Utilities.
@Project   : 
@Author    : layton
"""
import logging
import sys, os
from config.config import Configuration
BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE)

DEFAULT_LOG_CONF = {
    'level': logging.INFO,
    'format': '%(asctime)s %(levelname)s %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

LOG_LEVELS = {
    'debug': logging.DEBUG, 
    'info': logging.INFO, 
    'warn': logging.WARN, 
    'error': logging.ERROR, 
    'critical': logging.CRITICAL}

class LoggerFactory():      
    def __init__(self):
        self.log_level = DEFAULT_LOG_CONF.get('level')
        self.log_format = DEFAULT_LOG_CONF.get('format')
        self.log_date_format = DEFAULT_LOG_CONF.get('date_format')

        # get configured log configuration params
        configd_param = Configuration().getLogConfig()
        
        # get log level from config
        if configd_param.get('level') is None:
            pass
        elif configd_param.get('level').lower() in LOG_LEVELS.keys():
            self.log_level = LOG_LEVELS.get(configd_param.get('level').lower())
        else:
            raise Exception('config.py config log error')

        # get log format from config
        if configd_param.get('format') is not None:
            self.log_format = configd_param.get('format')

        # get log date format from config
        if configd_param.get('date_format') is not None:
            self.log_date_format = configd_param.get('date_format')

    def getLogger(self, *args):
        if len(args) > 1:
            raise Exception('too much function args')

        if len(args) == 0:
            logging.basicConfig(
                level = self.log_level,
                format = self.log_format,
                datefmt = self.log_date_format)

            return logging.getLogger()
        
        # set module name to log format
        if len(args) == 1:
            logging.basicConfig(
                level = self.log_level,
                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt = self.log_date_format )
         
            return logging.getLogger(args[0])
