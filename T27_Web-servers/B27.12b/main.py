import cgi
from string import Template


def separate_digits_and_chars(string):
    digits = ""
    chars = ""

    for char in string:
        if char.isdigit():
            digits += char + " "
        else:
            chars += char + " "

    return digits, chars


def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        digits, chars = separate_digits_and_chars(string)

        start_response("200 OK",
                       [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/result.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(digits=digits, chars=chars)
    else:
        start_response("404 NOT FOUND",
                       [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8005

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
