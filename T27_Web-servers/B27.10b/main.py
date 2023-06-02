import cgi
from string import Template

def remove_brackets(string):
    inside_brackets = False
    result = []

    for char in string:
        if char == "(":
            inside_brackets = True
        elif char == ")":
            inside_brackets = False
        elif not inside_brackets:
            result.append(char)

    return "".join(result)

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")

        if string == "":
            result = ""

        else:
            if remove_brackets(string):
                answer = "результат"
                result = "<h1>{} - {}</h1>".format(remove_brackets(string), answer)
        start_response("200 OK",[("Content-type", "text/html; "
                                                  "charset=utf-8"), ])
        with open("templates/index.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND",
                       [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()
    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8015

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
