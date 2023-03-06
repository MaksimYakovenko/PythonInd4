import cgi
import json
from wsgiref.simple_server import make_server

from core import Passenger, save_route, save_passenger

HOST = ''
PORT = 8002
HEADERS = [
    ('Content-type', 'text/html; charset=utf-8'),
]


def process_route(departure, arrival, distance):
    with open('./html/route.html', 'r', encoding='utf-8') as f:
        route_html = f.read()
    route_info = ''
    if departure and arrival and distance:
        save_route(departure, arrival, distance)
        route_info = f'<h2>Наступний маршрут було додано: {departure} - {arrival}, відстань {distance}км.</h2>'
    return route_html.format(route_info=route_info)


def process_passenger(last_name, name, middle_name):
    with open('./html/passenger.html', 'r', encoding='utf-8') as f:
        passenger_html = f.read()
    passenger_info = ''
    if last_name and name and middle_name:
        save_passenger(last_name, name, middle_name)
        passenger_info = (
            '<h2>Пасажира було додано:</h2><pre>'
            f'    ПІБ: {last_name} {name} {middle_name}</pre>'
        )
    return passenger_html.format(passenger_info=passenger_info)


def application(environ, start_response):
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    path = environ.get('PATH_INFO', '')
    if path == '/':
        with open('./html/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        option_template = '<option value="{value}">{name}</option>'
        route_options = []
        with open('./data/routes.json', 'r') as f:
            txt = f.read()
            routes = json.loads(txt if txt else '[]')
            for r in routes:
                value = f'{r["departure"]} - {r["arrival"]}'
                name = f'{r["departure"]}, {r["arrival"]}, {r["distance"]}'
                route_options.append(option_template.format(value=value, name=name))
        passenger_options = []
        with open('./data/passengers.json', 'r') as f:
            txt = f.read()
            passengers = json.loads(txt if txt else '[]')
            for p in passengers:
                value = f'{p["last_name"]} {p["name"]} {p["middle_name"]}'
                name = f'{p["last_name"]} {p["name"]} {p["middle_name"]}'
                passenger_options.append(option_template.format(value=value, name=name))
        result_info = ''
        route = form.getfirst('route', '').strip()
        passenger_name = form.getfirst('passenger', '').strip()
        if route and passenger_name:
            departure, arrival = route.split(' - ')
            passenger_obj = Passenger(passenger_name, departure, arrival)
            price = passenger_obj.get_ticket_price()
            result_info = (
                '<h2>Інфоманція за проїзд:</h2>\n<pre>'
                f'    ПІБ: {passenger_name}\n'
                f'    Маршрут: Відправлення: {departure}, Прибуття: {arrival}\n'
                f'    Ціна за квиток: {price}грн.</pre>'
            )
        html_content = html_content.format(routes='\n'.join(route_options), passengers='\n'.join(passenger_options),
                                           result_info=result_info)
        status = '200 OK'
    elif path == '/route':
        departure = form.getfirst('departure', '').strip()
        arrival = form.getfirst('arrival', '').strip()
        distance = form.getfirst('distance', '').strip()
        html_content = process_route(departure, arrival, distance)
        status = '200 OK'
    elif path == '/passenger':
        last_name = form.getfirst('last_name', '').strip()
        name = form.getfirst('name', '').strip()
        middle_name = form.getfirst('middle_name', '').strip()
        html_content = process_passenger(last_name, name, middle_name)
        status = '200 OK'
    else:
        with open('./html/error.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        status = '404 Page not found'
    start_response(status, HEADERS)
    return [bytes(html_content, encoding='utf-8')]


if __name__ == '__main__':
    print(f'Локальний веб-сервер запущено на http://localhost:{PORT}')
    httpd = make_server(HOST, PORT, application)
    httpd.serve_forever()
