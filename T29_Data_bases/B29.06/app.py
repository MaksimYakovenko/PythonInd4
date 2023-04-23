import cgi
import os.path
import sqlite3
import openpyxl
from wsgiref.simple_server import make_server
from core import DB_PATH, Passenger, get_passengers, get_routes, Route, \
    DeletePassenger, UpdatePassenger, get_passenger_id

HOST = ''
PORT = 8020
HEADERS = [
    ('Content-type', 'text/html; charset=utf-8'),
]

def application(environ, start_response):
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    path = environ.get('PATH_INFO', '')
    if path == '/':
        with open('html/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        option_template = '<option value="{value}">{name}</option>'
        route_options = []
        routes = get_routes()
        for route in routes:
            route_options.append(option_template.format(value=route, name=route))
        passenger_options = []
        passengers = get_passengers()
        for passenger in passengers:
            passenger_options.append(option_template.format(value=passenger, name=passenger))
        html_content = html_content.format(routes='\n'.join(route_options),passengers='\n'.join(passenger_options))
        status = '200 OK'
    elif path == '/result':
        passenger = form.getfirst('passenger', '').strip()
        route = form.getfirst('route', '').strip()
        last_name, name, middle_name = passenger.split(' ')
        departure, arrival, distance = route.split(' ')
        passenger_obj = Passenger(last_name, name, middle_name, departure, arrival)
        price = passenger_obj.get_ticket_price()
        with open('html/result.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        html_content = html_content.format(last_name=last_name, name=name, middle_name=middle_name, departure=departure,
                                           arrival=arrival, price=price)
        status = '200 OK'

    elif path == '/add_route':
        departure = form.getfirst('departure', '').strip()
        arrival = form.getfirst('arrival', '').strip()
        distance = form.getfirst('distance', '').strip()
        with open('html/add_route.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        route_info = ''
        if departure and arrival and distance:
            Route.add_route(departure, arrival, distance)
            route_info = f'<h2>Наступний маршрут було додано: {departure} - {arrival}, відстань {distance}км.</h2>'
        html_content = html_content.format(route_info=route_info)
        status = '200 OK'

    elif path == '/add_passenger':
        last_name = form.getfirst('last_name', '').strip()
        name = form.getfirst('name', '').strip()
        middle_name = form.getfirst('middle_name', '').strip()
        with open('html/add_passenger.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        passenger_info = ''
        if last_name and name and middle_name:
            Passenger.add_passenger(last_name, name, middle_name)
            passenger_info = (
                '<h2>Пасажира було додано:</h2><pre>'
                f'    ПІБ: {last_name} {name} {middle_name}</pre>'
            )
        html_content = html_content.format(passenger_info=passenger_info)
        status = '200 OK'

    elif path == '/delete_passenger':
        passenger = form.getfirst('passenger', '').strip()
        with open('html/delete_passenger.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        option_template = '<option value="{value}">{name}</option>'
        passenger_options = []
        passengers = get_passenger_id()
        for p in passengers:
            passenger_options.append(option_template.format(value=p, name=p))

        delete_info = ''
        if passenger:
            passenger_obj = DeletePassenger(p)
            passenger_obj.delete_passenger(p)
            delete_info = (
                f'<h2>Пасажира з id {passenger} було видалено:</h2><pre>'
            )
        html_content = html_content.format(delete_info=delete_info, passengers='\n'.join(passenger_options))
        status = '200 OK'

    elif path == '/update_passenger':
        passenger = form.getfirst('passenger', '').strip()
        last_name = form.getfirst('last_name', '').strip()
        name = form.getfirst('name', '').strip()
        middle_name = form.getfirst('middle_name', '').strip()
        with open('html/update_passenger.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        option_template = '<option value="{value}">{name}</option>'
        passenger_options = []
        passengers = get_passenger_id()
        for p in passengers:
            passenger_options.append(option_template.format(value=p,name=p))

        passenger_info = ''
        if passenger and last_name and name and middle_name:
            passenger_obj = UpdatePassenger(passenger, last_name, name, middle_name)
            passenger_obj.update_passenger()
            passenger_info = (
                '<h2>Пасажира було оновлено:</h2><pre>'
                f'    ПІБ: {last_name} {name} {middle_name}</pre>'
            )
        html_content = html_content.format(passenger_info=passenger_info,passengers='\n'.join(passenger_options))
        status = '200 OK'
    else:
        with open('html/error.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        status = '404 Page not found'
    start_response(status, HEADERS)
    return [bytes(html_content, encoding='utf-8')]


def from_excel(xlsx_filename):
    wb = openpyxl.load_workbook(xlsx_filename)
    sheets = {}
    for ws in wb:
        sheets[ws.title] = [
            [cell.value for cell in row]
            for row in ws.rows
        ]
    return sheets


def restore_db(xlsx_filename, db_filename):
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.executescript(
        """
        CREATE TABLE "routes" ( 
          "departure" TEXT, 
          "arrival" TEXT, 
          "distance" INTEGER
        );
        CREATE TABLE "passengers" ( 
          "p_id" INTEGER NOT NULL UNIQUE,
          "last_name" TEXT, 
          "name" TEXT, 
          "middle_name" TEXT,
          PRIMARY KEY("p_id" AUTOINCREMENT)
        );
        """
    )
    sheets = from_excel(xlsx_filename)
    curs.executemany(
        """INSERT INTO "passengers" VALUES (?, ?, ?, ?)""",
        sheets["passengers"][1:]
    )
    curs.executemany(
        """INSERT INTO "routes" VALUES (?, ?, ?)""",
        sheets["routes"][1:]
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    xlsx = 'data/data.xlsx'
    restore_db(xlsx, DB_PATH)
    print(f'Локальний веб-сервер запущено на http://localhost:{PORT}')
    httpd = make_server(HOST, PORT, application)
    httpd.serve_forever()
