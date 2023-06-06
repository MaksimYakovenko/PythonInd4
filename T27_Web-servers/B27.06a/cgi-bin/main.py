import cgi
from string import Template


def find_elements(a, b):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return None

    result = [x for x in range(int(a), int(b) + 1)]
    return result


if __name__ == '__main__':
    form = cgi.FieldStorage()
    a = form.getfirst("a", "")
    b = form.getfirst("b", "")

    elements = find_elements(a, b)
    if elements is not None:
        result = " ".join(str(x) for x in elements)
    else:
        result = "Помилка: Некоректні дані"

    with open("result.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(result=result)

    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
