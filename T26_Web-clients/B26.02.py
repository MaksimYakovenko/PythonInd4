from urllib.request import urlopen, Request
import re
from datetime import datetime

TIME_REGEX = r"draw_clock\('clock_id',(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\);"


def find_time():
    url = "https://time.online.ua/ukr/in/kyiv/"
    request = Request(url, headers={"user-agent":"123"})
    try:
        response = urlopen(request)
        html = str(response.read(), encoding="utf-8", errors="ignore")
        matches = re.findall(TIME_REGEX, html)
        if matches:
            year, month, day, hour, minute, second = matches[0]
            site_time = datetime(int(year), int(month), int(day), int(hour),
                                 int(minute), int(second))
            print("Поточний час на сайті:", site_time.strftime("%Y-%m-%d %H:%M:%S"))

            local_time = datetime.now()
            print("Поточний час на комп'ютері:",
                  local_time.strftime("%Y-%m-%d %H:%M:%S"))

            if site_time == local_time:
                print("Час на сайті відповідає локальному часу")
            else:
                print("Час на сайті не відповідає локальному часу")
        else:
            print("Не вдалося знайти час на сайті")

    except Exception as e:
        print("Помилка при з'єднанні з сайтом:", str(e))

if __name__ == '__main__':
    find_time()
