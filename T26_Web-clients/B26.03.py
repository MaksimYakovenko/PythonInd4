from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib.error import HTTPError
import re
from datetime import datetime

TIME = r'<noscript>(.*?)</noscript>'

def find_date():
    url = "https://godinnik.com/"
    path = f"/time/київ/"
    time_url = url + quote(path)
    try:
        request = Request(time_url, headers={"user-agent":""})
        response = urlopen(request)
        html = str(response.read(), encoding="utf-8", errors="ignore")
        # print(html)
        right_time = re.findall(TIME, html)[-1]
        print("Час на сайті:", right_time)
        cur_time = datetime.today().strftime("%H:%M:%S")
        print("Час на коп'ютері", cur_time)
    except HTTPError as e:
        print(e)

if __name__ == '__main__':
    find_date()
