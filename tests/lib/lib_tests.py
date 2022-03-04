
"""Unit test library"""
import json
from urllib.request import Request, urlopen

JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

def ws_client(url, method=None, data=None):
    if not method:
        method = "PUT" if data else "GET"
    if data:
        data = json.dumps(data).encode("utf-8")
    headers = {"Content-type": JSON_CONTENT_TYPE} \
                if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

