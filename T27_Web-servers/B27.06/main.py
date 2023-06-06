import cgi
from string import Template


def find_elements(a, b):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return None

    result = [x for x in range(int(a), int(b) + 1)]
    return result


def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        a = form.getfirst("a", "")
        b = form.getfirst("b", "")

        elements = find_elements(a, b)
        if elements is not None:
            result = " ".join(str(x) for x in elements)
        else:
            result = "Помилка: Некоректні дані"

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/result.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8005

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
