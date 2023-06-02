import cgi
from string import Template

def remove_brackets(string):
    answer = ''
    add_to_answer = 1
    for char in string:
        if char == "(":
            add_to_answer = 0
        elif char == ")":
            add_to_answer = 1
        answer = answer + char if add_to_answer == 1 else answer
    return ''.join(answer.split(')'))

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    result = remove_brackets(string)
    with open("result.html", "r", encoding="utf-8") as file:
        page = Template(file.read()).substitute(result=result)

    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
