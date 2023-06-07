import cgi
from string import Template

def find_min_max(sequence):
    try:
        numbers = [float(x) for x in sequence.split()]
        if len(numbers) == 0:
            return None, None
        min_num = min(numbers)
        max_num = max(numbers)
        return min_num, max_num
    except ValueError:
        return None, None

def highlight_min_max(sequence, min_num, max_num):
    if min_num is None or max_num is None:
        return None
    highlighted_sequence = ""
    for num in sequence.split():
        if float(num) == min_num:
            highlighted_sequence += f"<span style='color: red;'>{num}</span> "
        elif float(num) == max_num:
            highlighted_sequence += f"<span style='color: blue;'>{num}</span> "
        else:
            highlighted_sequence += f"{num} "
    return highlighted_sequence

def application(environ, start_response):
    if environ.get("PATH_INFO", "").lstrip("/") == "":
        form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
        sequence = form.getfirst("sequence", "")
        min_num, max_num = find_min_max(sequence)
        highlighted_sequence = highlight_min_max(sequence, min_num, max_num)
        start_response("200 OK",[("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/index.html", encoding="utf-8") as f:
            page = Template(f.read()).substitute(sequence=sequence,
                                                 min_num=min_num,
                                                 max_num=max_num,
                                                 highlighted_sequence=highlighted_sequence)
    else:
        start_response("404 NOT FOUND",[("Content-type", "text/html; charset=utf-8"), ])
        with open("templates/error_404.html", encoding="utf-8") as f:
            page = f.read()

    return [bytes(page, encoding="utf-8")]

HOST = ""
PORT = 8021

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"Локальний веб-сервер запущено на http://localhost:{PORT}")
    make_server(HOST, PORT, application).serve_forever()
