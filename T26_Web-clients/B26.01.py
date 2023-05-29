from urllib.request import urlopen
import re
from datetime import datetime

TIME = r'<span id=ct class=h1>(.+?)</span>'


def find_time():
    url = "https://www.timeanddate.com/worldclock/ukraine/kyiv"
    response = urlopen(url)
    html = str(response.read(), encoding="utf-8", errors="ignore")
    # print(html)
    date = re.findall(TIME, html)
    # print(date)
    right_time = " ".join(date)
    print("Поточний час на сайті:", right_time)
    cur_time = datetime.today().strftime("%H:%M:%S")
    print("Поточний час на комп'ютері:", cur_time)

if __name__ == '__main__':
    find_time()
