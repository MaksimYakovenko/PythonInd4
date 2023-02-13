import cgi
from string import Template

def calculate_dispersion(str1):
    lst = [float(k) for k in str1.split(",")]
    arith_mean = sum(lst) / len(lst) if len(lst) != 0 else 0
    diff = [(v - arith_mean) for v in lst]
    mod_diff = [abs(d) if d < 0 else d for d in diff]
    return mod_diff

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form["string"].value
    result = calculate_dispersion(string)
    # answer = 'обчислена дисперсія' if calculate_dispersion(string) else \
    #     'дисперсію неможливо обчислити'
    #
    # result = string + ' - ' + answer
    with open("resultpage.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(result=result)

    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

    print("Content-type: text/html charset=utf-8\n")
    print(page)
