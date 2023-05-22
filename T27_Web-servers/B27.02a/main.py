import cgi
from string import Template

def find_common_words(string1, string2):
    words1 = set(string1.split())
    words2 = set(string2.split())
    common_words = words1.intersection(words2)
    return " ".join(common_words)

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string1 = form.getfirst("string1", "")
    string2 = form.getfirst("string2", "")
    result = find_common_words(string1, string2)
    with open("result.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(result=result)

    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
