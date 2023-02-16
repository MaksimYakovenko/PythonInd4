import cgi
from string import Template

def check_for_words(string):
    s = ""
    for char in string:
        if char.isalpha():
            s += char.lower()
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
    if check_for_words(string):
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
