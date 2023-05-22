import cgi
from string import Template

def find_common_words(string1, string2):
    words1 = set(string1.split())
    words2 = set(string2.split())
    common_words = words1.intersection(words2)
    return common_words

def application(environ, start_response):
    if environ["PATH_INFO"].lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string1 = form.getfirst("string1", "")
        string2 = form.getfirst("string2", "")
        common_words = find_common_words(string1, string2)

        result_string = ", ".join(common_words)

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/index.html", encoding="utf-8") as f:
            page_template = Template(f.read())
            page = page_template.substitute(result=result_string)
    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8")])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8007

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
