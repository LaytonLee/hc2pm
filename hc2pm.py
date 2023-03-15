#! /usr/bin/python3
# -*- coding: UTF-8 -*-

"""hc2pm.
@Project   : 将 HttpCanary App 导出的request.json转换为Postman可识别导入的json格式
@Author    : layton
"""

import os
from utils.log_utils import LoggerFactory
import json
from urllib.parse import unquote
import argparse

parser = argparse.ArgumentParser(
        prog="hc2pm",
        description="transform HttpCanary export request json format into postman import reqest format")
parser.add_argument("--input", "-i", help="待转换的文件或目录", required=True)
parser.add_argument("--collection", "-c", help="postman的collection名称", required=True)
parser.add_argument("--output", "-o", help="输出文件名(*.json)", required=True)
args = parser.parse_args()

logger = LoggerFactory().getLogger()

SCHEMAS = {
    "v2": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
}

class PostmanData():
    class PMRequest():
        class HeaderItem(): 
            def __init__(self, key:str = None, value:str = None, type:str = None):
                self.key = key
                self.value = value
                self.type = type
            
            def __repr__(self) -> str:
                return f"{{ key={self.key}, value={self.value}, type={self.type} }}"


        class Url():
            def __init__(self, raw:str = None):
                self.raw = raw

                self.protocal = raw.split("://")[0]
                self.host = raw.split("://")[1].split("/")[0].split(".")
                self.path = raw.split("://")[1].split("?")[0].split("/")[1:]
               
                self.query = list(map(lambda x: {"key": x.split("=")[0], "value": x.split("=")[1]}, raw.split("?")[1].split("&")))

            def __repr__(self) -> str:
                return f"{{ raw={self.raw}, protocal={self.protocal}, host={self.host}, path={self.path}, query={self.query} }}"


        def __init__(self, name:str = None, method:str = None, headers:list[HeaderItem] = None, url:Url = None):
            self.name = name
            
            self.request: dict() = {}
            self.request["method"] = method
            self.request["header"] = headers
            self.request["url"] = url

            self.response = list()

        def __repr__(self) -> str:
            return f"name={self.name}, request={self.request}, url={self.request['url']}"

    def __init__(self, collection_name:str = None, scheme_version:str = "v2", items:list[PMRequest] = None):
        self.info: dict() = {}
        self.info["_postman_id"] = "aaa"
        self.info["name"] = collection_name
        self.info["schema"] = SCHEMAS.get(scheme_version)

        self.item = items

    def __repr__(self) -> str:
        return f"{{ info={self.info}, item={self.item} }}"
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

        
def hc2pm_file(file_path: str, request_name: str) -> PostmanData.PMRequest:
    if not os.path.exists(file_path):
        raise IOError(f"No such file: {file_path}")
        return 

    hc_str = ""
    with open(file_path, 'r') as f:
        hc_str = f.read()
    
    hc_json = json.loads(hc_str)
    headers: list[PostmanData.PMRequest.HeaderItem()] = []
    for i_key, i_value in hc_json.get("headers").items():
        header_item = PostmanData.PMRequest.HeaderItem(i_key, unquote(i_value), "default")
        headers.append(header_item)
    
    url = PostmanData.PMRequest.Url(unquote(hc_json.get("url")))
    method = hc_json.get("method")
    
    return PostmanData.PMRequest(request_name, method, headers, url) 

def hc2pm_dir(dir):
    pm_reqs: list[PostmanData.PMRequest] = []
    
    for item in os.listdir(dir):
        sub_path = os.path.join(dir, item)

        tmp_item: dict() = {}
        if os.path.isdir(sub_path):
            tmp_item["name"] = item
            tmp_item["item"] = hc2pm_dir(sub_path)
            pm_reqs.append(tmp_item) 
        
        if sub_path[-4:] == "json":
            pm_req = hc2pm_file(sub_path, item.split(".")[0])
        
            pm_reqs.append(pm_req)
        
    return pm_reqs

def hc2pm_collection(collection_name, hc_path):
    if not os.path.exists(hc_path):
        raise IOError(f"No such path: {hc_path}")
   
    pm_req_data:list = None
    if os.path.isfile(hc_path):
        pm_req_data = hc2pm_file(hc_path)

    if os.path.isdir(hc_path):
        pm_req_data = hc2pm_dir(hc_path)

    pm_coll_data = PostmanData(collection_name, "v2", pm_req_data) 

    return pm_coll_data
    
if __name__ == "__main__":
    try:
        pm_coll_data = hc2pm_collection(args.collection, args.input)
        with open(args.output, 'w') as f:
            f.write(pm_coll_data.to_json())
    except Exception as e:
        logger.error(e)
