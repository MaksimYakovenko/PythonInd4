from urllib.request import urlopen, Request  # Функція для отримання веб-сторінки з мережі
import re
from datetime import datetime

TIME = r'<time id="clock">(?P<TIME>.+)</time>'

def find_time(city):
    url = "https://time.is/"
    main_url = url + city
    print(main_url)
    request = Request(main_url, headers={"user-agent":"123"})
    response = urlopen(request)
    html = str(response.read(), encoding="utf-8", errors="ignore")
    # print(html)
    date = re.findall(TIME, html)
    # print(date)
    right_time = " ".join(date)
    # print(date_str)
    print("Поточний час : ", right_time)
    cur_time = datetime.today().strftime("%H:%M:%S")
    print("Поточний час на комп'ютері: ", cur_time)

if __name__ == '__main__':
    find_time("Kyiv")
