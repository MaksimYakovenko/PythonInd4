# Побудувати програму, що працює у середовищі веб-сервера для розв'язання 
# задачі. Ввести рядок та повернути JSON, що містять всі його слова у порядку спадання

import cgi
import json
from string import Template

def sort_words(string):
    words = string.split()
    sorted_words = sorted(words, reverse=True)
    return sorted_words

def application(environ, start_response):
    if environ["PATH_INFO"].lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        sorted_words = sort_words(string)

        response_data = {
            "string": string,
            "sorted_words": sorted_words
        }
        response_json = json.dumps(response_data)

        start_response("200 OK", [("Content-type", "text/html; "
                                                   "charset=utf-8")])
        with open("templates/index.html", encoding="utf-8") as f:
            page_template = Template(f.read())
            page = page_template.substitute(string=string, sorted_words=response_json)

        return [bytes(page, encoding="utf-8")]
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()
        return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8035

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
