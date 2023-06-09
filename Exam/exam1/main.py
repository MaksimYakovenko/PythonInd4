import cgi
from string import Template

def replace_zeros_ones(string):
    replaced_string = ""
    for char in string:
        if char == '0':
            replaced_string += '1'
        elif char == '1':
            replaced_string += '0'
        else:
            replaced_string += char
    return replaced_string

def application(environ, start_response):
    if environ["PATH_INFO"].lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        replaced_string = replace_zeros_ones(string)

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/index.html", encoding="utf-8") as f:
            page_template = Template(f.read())
            page = page_template.substitute(string=string,
                                            replaced_string=replaced_string)
    else:
        start_response("404 NOT FOUND",
                       [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8025

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
