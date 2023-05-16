import cgi
from string import Template

def difference(string1, string2):
    words1 = set(string1.split())
    words2 = set(string2.split())
    unique_words = words1 - words2
    return " ".join(unique_words)

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string1 = form.getfirst("string1", "")
        string2 = form.getfirst("string2", "")
        if string1 == "" and string2 == "":
            result = ""
        elif string1 == string2:
            answer = "слова в першому і в другому полі однакові"
            result = "<h1>{}</h1>".format(answer)
        else:
            if difference(string1, string2):
                answer = "знайдене слово"
                result = "<h1>{} - {}</h1>".format(difference(string1, string2), answer)
        start_response("200 OK",[("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/index.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)
    else:
        start_response("404 NOT FOUND",
                       [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()
    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8000

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
