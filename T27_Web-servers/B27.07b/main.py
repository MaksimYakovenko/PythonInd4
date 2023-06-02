import cgi
from string import Template


def compute_scalar_product(vector1, vector2):
    if len(vector1) != len(vector2):
        return None

    scalar_product = sum(x * y for x, y in zip(vector1, vector2))
    return scalar_product


def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        vector1 = form.getfirst("vector1", "")
        vector2 = form.getfirst("vector2", "")

        try:
            vector1 = [float(x) for x in vector1.split()]
            vector2 = [float(x) for x in vector2.split()]
        except ValueError:
            result = "Помилка: Некоректні дані"
        else:
            scalar_product = compute_scalar_product(vector1, vector2)
            if scalar_product is not None:
                result = f"Скалярний добуток векторів: {scalar_product}"
            else:
                result = "Помилка: Розміри векторів не співпадають"

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/result.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8010

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
