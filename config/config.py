#! /usr/bin/python3
# -*- coding: UTF-8 -*-

'''Configuration.
@Project   : 
@Author    : layton
'''

class Configuration():
    def __init__(self):
        # log config
        self.log_config = {
            'level': 'info'
            # 'format': '%(asctime)s %(levelname)s %(message)s',
            # 'date_format': '%Y-%m-%d %H:%M:%S'
        }
    
    def getLogConfig(self) -> dict:
        return self.log_config