from urllib.request import urlopen # Функція для отримання веб-сторінки з мережі
import re # Імпортуємо бібліотеку для регулярних виразів
import openpyxl # Імпортуємо бібліотеку для роботи з програмую Microsoft Excel

# Шаблон регулярного виразу, який знаходить дату
DATE = r"<span>(?P<DATE_NAME>.+)</span>"
# Шаблон регулярного виразу, який знаходить значення температури
TEMP = r"<span>(?P<DEG>.+)&deg;</span>"
# Шаблон регулярного виразу, який знаходить значення вологості
HUMIDITY = r"<span>(?P<HUMIDITY_VALUE>.+)&%</span>" # Вологість

def find_date(html):
    """Функція, яка знаходить та повертає значення сьогоднішньої дати"""
    re_list = re.findall(DATE, html)
    return re_list

def find_temp(html):
    """Функція, яка знаходить та повертає значення температури"""
    re_list = re.findall(TEMP, html)
    return re_list

def find_humidity(html):
    """Функція, яка знаходить та повертає значення вологості"""
    re_list = re.findall(HUMIDITY, html)
    return re_list

def make_url(city):
    """Функція, яка формує посилання для заданого міста"""
    main_url = "https://www.meteoprog.com/ua/meteograms/"
    # city = "Kyiv"
    full_url = main_url + city
    return full_url

def get_html(url):
    """ Повертає розкодавані дані веб-сторінки за заданою адресою."""
    return str(urlopen(url).read(), encoding="utf-8", errors="ignore")

def fix_html(html):
    """ Весь код написано в один рядок (!) Шукаємо кінці рядків вигляду '...> '   """
    html = "> \n".join(html.split("> "))
    return html

def main_function(city, file):
    url = make_url(city)
    html = get_html(url)
    html = fix_html(html)

    date_list, temp_list, humidity_list = find_date(html), find_temp(html), find_humidity(html)
    wb = openpyxl.Workbook()
    ws = wb["Sheet"]
    ws.append(["Дата", "Температура", "Вологість"])
    for i in range(8):
        ws.append([date_list[i - 1]])
    wb.save("output.xlsx")

if __name__ == '__main__':
    main_function("Kyiv", "output.xlsx")
    
