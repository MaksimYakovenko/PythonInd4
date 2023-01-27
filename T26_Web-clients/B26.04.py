import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

url = "https://time.is/Kyiv"

response = requests.get(url, headers={"user-agent": "123"})
soup = BeautifulSoup(response.text, 'lxml')

time = soup.find("time", id="clock").text.split()
# print(time)
right_time = " ".join(time)

# print(right_time)
time_str = datetime.strptime(right_time, "%H:%M:%S")
# print(time_str)

print("Поточний час на сайті: ", right_time)

cur_time = datetime.today().strftime("%H:%M:%S")
print("Поточний час на комп'ютері: ", cur_time)

