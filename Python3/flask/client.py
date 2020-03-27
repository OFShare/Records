#
# Created by OFShare on 2020-03-27
#

import requests
import urllib, json, base64

url = 'http://localhost:8123'

d = {"name": 'Acui'} 
# d = urllib.parse.urlencode(d)

ret = requests.get(url)
print("\n==========get===========")
print(ret)
ret_data = json.loads(ret.text)
print("return data: ", ret_data)

ret = requests.post(url, data=d, headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
print("\n==========post===========")
print(ret)
ret_data = json.loads(ret.text)
print("return data: ", ret_data)

