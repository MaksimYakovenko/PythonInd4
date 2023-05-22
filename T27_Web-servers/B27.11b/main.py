import cgi
from string import Template


def find_longest_sequence(string):
    if not string:
        return None, None

    current_char = ""
    current_length = 0
    max_char = ""
    max_length = 0

    for char in string:
        if char == current_char:
            current_length += 1
        else:
            current_char = char
            current_length = 1

        if current_length > max_length:
            max_char = current_char
            max_length = current_length

    return max_char, max_length


def highlight_longest_sequence(string, max_char):
    highlighted_string = ""
    for char in string:
        if char == max_char:
            highlighted_string += '<span style="color: blue;">{}</span>'.format(char)
        else:
            highlighted_string += char
    return highlighted_string


def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")

        max_char, max_length = find_longest_sequence(string)

        if max_char is not None and max_length is not None:
            highlighted_string = highlight_longest_sequence(string, max_char)
            result = "<h1>{}</h1>".format(highlighted_string)
        else:
            result = ""

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/index.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8004

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
