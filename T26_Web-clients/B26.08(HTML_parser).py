from html.parser import HTMLParser
from urllib.request import urlopen

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.count_humidity = 0
        self.in_span_temperature = False
        self.in_span_humidity = False
        self.in_div = False

    def handle_starttag(self, tag, attrs):
       if tag == "span" and attrs == [("class", "today-hourly-weather__temp")]:
           self.in_span_temperature = True
       if tag == "span" and attrs == [("title", "Вологість")]:
           self.in_span_humidity = True
       if tag == "div" and attrs == [("class", "day-in-history__date")]:
           self.in_div = True

    def handle_data(self, data):
        if self.in_div:
            print(data)
        if self.in_span_temperature:
            print(data, end=" ")
        if self.in_span_humidity:
            self.count_humidity += 1
            while self.count_humidity == 5:
                continue
            print(data, end=" ")

    def handle_endtag(self, tag):
        if tag == "span":
            self.in_span_temperature = False
        if tag == "div":
            self.in_div = False
        if tag == "span":
            self.in_span_humidity = False

if __name__ == '__main__':
    site = "https://www.meteoprog.com/ua/weather/"
    city = "Kyiv"
    url = site + city
    response = urlopen(url)
    html = str(response.read(), encoding="utf-8", errors="ignore")
    tvp = MyHTMLParser()
    tvp.feed(html)
