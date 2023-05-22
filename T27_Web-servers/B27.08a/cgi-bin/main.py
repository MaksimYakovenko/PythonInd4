import cgi
from string import Template


def count_sign_changes(sequence):
    if not sequence:
        return 0

    changes = 0
    prev_sign = 0

    for num in sequence:
        num = int(num)
        curr_sign = 1 if num > 0 else -1

        if prev_sign != 0 and prev_sign != curr_sign:
            changes += 1

        prev_sign = curr_sign
    return changes

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "").split(",")
    result = count_sign_changes(string)
    with open("result.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(result=result)

    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
