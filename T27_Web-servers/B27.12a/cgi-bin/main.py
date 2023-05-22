import cgi
from string import Template


def separate_digits_and_chars(string):
    digits = ""
    chars = ""

    for char in string:
        if char.isdigit():
            digits += char + " "
        else:
            chars += char + " "

    return digits, chars

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    digits, chars = separate_digits_and_chars(string)
    with open("result.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(digits=digits, chars=chars)

    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
