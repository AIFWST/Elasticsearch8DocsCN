import json
import requests
from config.setting import configDICT

def get_token():
    auth_url = "https://edge.microsoft.com/translate/auth"
    auth_headers = {
        "Content-Type": "text/plain; charset=utf-8"
    }
    Authorization = requests.get(auth_url, headers=auth_headers).text
    return Authorization

def url_option():
    url = configDICT["edge_url"]
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Access-Control-Request-Headers": "authorization,content-type",
        "Access-Control-Request-Method": "POST",
        "Origin": "null",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": configDICT["User-Agent"]}
    requests.options(url, headers=headers)


def get_translate(token, body):
    translate_url = configDICT["edge_url"]
    translate_headers = {
        "Authorization": "Bearer " + str(token),
        "Content-Length": str(len(json.dumps(body, separators=(",", ":")))),
        "Content-Type": "application/json",
        "User-Agent": configDICT["User-Agent"]
    }
    res = requests.post(translate_url, headers=translate_headers, data=json.dumps(body, separators=(",", ":")), verify=False)
    return res



