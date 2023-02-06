import cgi
from string import Template


def calculate_dispersion(string):
    arith_mean = sum(string) / len(string)
    diff = [(v - arith_mean) for v in string]
    sqr_diff = [d ** 2 if d < 0 else d for d in diff]
    return sqr_diff

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    result = calculate_dispersion(string)
    with open("resultpage.html", encoding="utf-8") as f:
        page = Template(f.read().substitute(result=result))

    import os

    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

    print("Content-type: text/html charset=utf-8\n")
    print(page)
