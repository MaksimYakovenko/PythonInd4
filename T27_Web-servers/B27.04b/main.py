import cgi
import re
from string import Template

INCORRECT_DATA = r"[a-z]+"

def incorrect_data(string):
    s = re.findall(INCORRECT_DATA, string)
    return s



def calculate_dispersion(string):
    lst_value = [float(k) for k in string.split(",")]
    arith_mean = sum(lst_value) / len(lst_value) if len(lst_value) != 0 else 0
    diff = [(v - arith_mean) for v in lst_value]
    mod_diff = [abs(d) if d < 0 else d for d in diff]
    mod_diff_str = ', '.join(map(str, mod_diff))
    return mod_diff_str


def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        string = form.getfirst("string", "")
        if incorrect_data(string):
            answer = "обчислити дисперсію неможливо"
            result = "<h1>{} - {}</h1>".format(string, answer)

        elif string == "":
            result = ""
        
        else:

            if calculate_dispersion(string):
                answer = "обчислена дисперсія"
                result = "<h1>{} - {}</h1>".format(calculate_dispersion(
                    string), answer)

        start_response("200 OK", [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/dispersion.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(result=result)


    else:
        start_response("404 NOT FOUND", [("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]


HOST = ""
PORT = 8000

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(" === Local WSGI webserver === ")
    make_server(HOST, PORT, application).serve_forever()