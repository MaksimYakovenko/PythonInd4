from urllib.request import urlopen, Request
import re
from datetime import datetime

TIME = r'<time id="clock">(?P<TIME>.+)</time>'

def find_time():
    url = "https://time.is/"
    city = "Kyiv"
    main_url = url + city
    request = Request(main_url, headers={"user-agent":"123"})
    response = urlopen(request)
    html = str(response.read(), encoding="utf-8", errors="ignore")
    # print(html)
    date = re.findall(TIME, html)
    # print(date)
    right_time = " ".join(date)
    # print(date_str)
    print("Поточний час на сайті: ", right_time)
    cur_time = datetime.today().strftime("%H:%M:%S")
    print("Поточний час на комп'ютері: ", cur_time)

if __name__ == '__main__':
    find_time()
