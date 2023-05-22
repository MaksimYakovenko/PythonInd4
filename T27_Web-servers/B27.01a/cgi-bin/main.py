import cgi
from collections import Counter
from string import Template


def count_word_occurrences(string):
    words = string.split()
    word_counts = Counter(words)
    return word_counts

if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst("string", "")
    word_counts = count_word_occurrences(string)
    result_string = ""
    for word, count in word_counts.items():
        result_string += f"<p>{word} - {count} рази(ів)</p>"

    with open("result.html", encoding="utf-8") as f:
        page_template = Template(f.read())
        page = page_template.substitute(result_string=result_string)

    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
