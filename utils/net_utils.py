#! /usr/bin/python3
# -*- coding: UTF-8 -*-

"""Net Utilities.
@Project   : 
@Author    : layton
"""

import requests
from requests.adapters import HTTPAdapter, Retry

def getRetrySession(**kwargs):
    session = requests.Session()
    # set Retry parameters, see detail: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry
    if len(kwargs) == 0:
        retries = Retry(total=5, connect=5, backoff_factor=5)
    else:
        retries = Retry(**kwargs)
    
    adapter = HTTPAdapter(max_retries = retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session