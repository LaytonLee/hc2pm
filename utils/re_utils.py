#! /usr/bin/python3
# -*- coding: UTF-8 -*-

"""Regex Utilities.
@Project   : 
@Author    : layton
"""

import re

def get_file_name_from_url(url: str, *suffixes):
    ''' 从url中获取文件名
        example url: https://xxx.com/1.jpg
    Parameters:
        url - url
        suffixes - 文件名后缀
    
    Returns:
        匹配到的文件名
    '''
    regex = '[\\w]+[\\.](' + '|'.join(suffixes) + ')'
    pattern = re.compile(regex, re.I)
    matcher = pattern.search(url)
    
    return matcher.group() if matcher != None else None

def get_params_from_js(js_content: str):
    ''' 获取js代码中的变量
    
    Parameters:
        js_content - js文本
    
    Returns:
        所有的匹配结果
    '''
    pattern = re.compile(r'(var\s+\w+\s*=.*?;)', re.MULTILINE | re.DOTALL)
    matcher = pattern.findall(js_content)
    
    return matcher if matcher != None else None
