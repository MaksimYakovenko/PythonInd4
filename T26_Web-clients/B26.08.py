from urllib.request import urlopen
import re

HUMIDITY = r'<span title="Вологість">(.*?)</span>'
TEMP = r'<span class="today-hourly-weather__temp">(.*?)</span>'
DATE = r'<div class="day-in-history__date">(.*?)</div>'

def find_humidity(html):
    re_list = re.findall(HUMIDITY, html, re.DOTALL)
    return re_list

def find_temp(html):
    re_list = re.findall(TEMP, html, re.DOTALL)
    return re_list

def find_date(html):
    re_list = re.findall(DATE, html, re.DOTALL)
    return re_list

def make_url(city):
    main_url = "https://www.meteoprog.com/ua/weather/"
    full_url = main_url + city
    return full_url

def get_html(url):
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")

def main_function(city):
    url = make_url(city)
    html = get_html(url)

    humidity_list, temp_list, date_list = find_humidity(html), find_temp(html), find_date(html)
    # print(date_list)
    # print(humidity_list)
    # print(temp_list)
    for i in range(1, 5):
        print(humidity_list[i - 1] + "  " + temp_list[i - 1] + "  " + date_list[i - 3])

if __name__ == '__main__':
    main_function("Kyiv")


    
