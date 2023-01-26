import time
from http.client import HTTPResponse
from datetime import datetime, timedelta
from urllib.request import urlopen, Request


url = "https://time.is/Kyiv"
request = Request(url, headers={"user-agent": "123"})
response = urlopen(request)
info = response.info()
# help(info)
# print(info)
# print("Status:", response.status)
# print("Encoding:", info.get_content_charset())
right_time = print("Час на сайті:", info.__getitem__("Expires"))
cur_time = print("Час на комп'ютері:", datetime.today().strftime("%a, %d %b %Y %H:%M:%S %Z"))

