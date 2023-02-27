from html.parser import HTMLParser
from urllib.request import urlopen, Request
from datetime import datetime

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_time = False

    def handle_starttag(self, tag, attrs):
        if tag == "time":
            self.in_time = True

    def handle_data(self, data):
        if self.in_time:
            print("Поточний час на сайті:", data)
            cur_time = datetime.today().strftime("%H:%M:%S")
            print("Поточний час на комп'ютері:", cur_time)

    def handle_endtag(self, tag):
        if tag == "time":
            self.in_time = False


if __name__ == '__main__':
    site = "https://time.is/"
    city = "Kyiv"
    url = site + city
    request = Request(url, headers={"user-agent":"123"})
    response = urlopen(request)
    html = str(response.read(), encoding="utf-8", errors="ignore")

    tvp = MyHTMLParser()
    tvp.feed(html)
