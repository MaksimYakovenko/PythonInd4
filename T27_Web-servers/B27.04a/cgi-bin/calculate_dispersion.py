import cgi
import re
from string import Template

INCORRECT_DATA = r"(?!,)[^0-9\s\.]+?"
COMMA = r"[\,^A-Za-zА-ЯІЇЄа-яіїє]+?"

def comma(string):
    s = re.findall(COMMA, string)
    return s

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

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    if not comma(string):
        with open("message_error.html", encoding="utf-8") as f:
            page = f.read()

    elif incorrect_data(string):
            answer = 'неможливо обчислити дисперсію'
            result_1 = string + ' - ' + answer
            with open("resultpage.html", encoding="utf-8") as f:
                page = Template(f.read()).substitute(result=result_1)
    else:
        if calculate_dispersion(string):
            answer = 'обчислена дисперсія'
            result_2 = calculate_dispersion(string) + ' - ' + answer
            with open("resultpage.html", encoding="utf-8") as f:
                page = Template(f.read()).substitute(result=result_2)

    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

    print("Content-type: text/html charset=utf-8\n")
    print(page)
