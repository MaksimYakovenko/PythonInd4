import cgi
from string import Template

def difference(string1, string2):
    words1 = set(string1.split())
    words2 = set(string2.split())
    unique_words = words1 - words2
    return " ".join(unique_words)

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string1 = form.getfirst("string1", "")
    string2 = form. getfirst("string2", "")
    result = difference(string1, string2)
    with open("resultpage.html", "r", encoding="utf-8") as file:
        page = Template(file.read()).substitute(result=result)

    if string1 == string2:
        with open("same_words.html", "r", encoding="utf-8") as file:
            page = file.read()
    import os
    if os.name == "nt":
        import sys, codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
