import cgi
from string import Template

def count_sign_changes(sequence):
    if not sequence:
        return 0

    changes = 0
    prev_sign = 0

    for num_str in sequence:
        num_str = num_str.strip()
        if num_str:
            try:
                num = int(num_str)
                curr_sign = 1 if num > 0 else -1

                if prev_sign != 0 and prev_sign != curr_sign:
                    changes += 1

                prev_sign = curr_sign
            except ValueError:
                pass

    return changes

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "").split(",")
        if string == [""]:
            result = 0
        else:
            result = count_sign_changes(string)

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8"), ])

        with open("templates/index.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8015

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
