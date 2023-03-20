import cgi
from wsgiref.simple_server import make_server
import xml.etree.ElementTree as ET

from core import Passenger, save_route, save_passenger

HOST = ''
PORT = 8003
HTML_HEADERS = [
    ('Content-type', 'text/html; charset=utf-8'),
]
XML_HEADERS = [
    ('Content-type', 'application/xml; charset=utf-8'),
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
        route_tree = ET.parse('./data/routes.xml')
        for route in route_tree.getroot().findall('route'):
            departure = route.find('departure').text.strip()
            arrival = route.find('arrival').text.strip()
            distance = route.find('distance').text.strip()
            value = f'{departure} - {arrival} - {distance}'
            name = f'{departure}, {arrival}, {distance}'
            route_options.append(option_template.format(value=value, name=name))
        passenger_options = []
        passenger_tree = ET.parse('./data/passengers.xml')
        for passenger in passenger_tree.getroot().findall('passenger'):
            last_name = passenger.find('last_name').text.strip()
            name = passenger.find('name').text.strip()
            middle_name = passenger.find('middle_name').text.strip()
            value = f'{last_name} {name} {middle_name}'
            name = f'{last_name} {name} {middle_name}'
            passenger_options.append(option_template.format(value=value, name=name))
        html_content = html_content.format(routes='\n'.join(route_options), passengers='\n'.join(passenger_options))
        status = '200 OK'
    elif path == '/result.xml':
        route = form.getfirst('route', '').strip()
        passenger_name = form.getfirst('passenger', '').strip()
        departure, arrival, distance = route.split(' - ')
        passenger_obj = Passenger(passenger_name, departure, arrival)
        price = passenger_obj.get_ticket_price()
        last_name, name, middle_name = passenger_name.split(' ')
        with open('./html/result.xml', 'r', encoding='utf-8') as f:
            html_content = f.read()
        html_content = html_content.format(last_name=last_name, name=name, middle_name=middle_name, departure=departure,
                                           arrival=arrival, distance=distance, price=price)
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
    start_response(status, XML_HEADERS if path.endswith('.xml') else HTML_HEADERS)
    return [bytes(html_content, encoding='utf-8')]


if __name__ == '__main__':
    print(f'Локальний веб-сервер запущено на http://localhost:{PORT}')
    httpd = make_server(HOST, PORT, application)
    httpd.serve_forever()
