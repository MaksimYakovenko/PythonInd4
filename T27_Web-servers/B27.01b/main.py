import cgi
from collections import Counter
from string import Template


def count_word_occurrences(string):
    words = string.split()
    word_counts = Counter(words)
    return word_counts


def application(environ, start_response):
    if environ["PATH_INFO"].lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        word_counts = count_word_occurrences(string)

        result_string = ""
        for word, count in word_counts.items():
            result_string += f"<p>{word} - {count} рази(ів)</p>"

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/index.html", encoding="utf-8") as f:
            page_template = Template(f.read())
            page = page_template.substitute(string=string, result_string=result_string)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8015

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
