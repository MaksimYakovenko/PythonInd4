import cgi
from string import Template

def find_min_max(sequence):
    try:
        numbers = [float(x) for x in sequence.split()]
        if len(numbers) == 0:
            return None, None
        min_num = min(numbers)
        max_num = max(numbers)
        return min_num, max_num
    except ValueError:
        return None, None

def highlight_min_max(sequence, min_num, max_num):
    if min_num is None or max_num is None:
        return None
    highlighted_sequence = ""
    for num in sequence.split():
        if float(num) == min_num:
            highlighted_sequence += f"<span style='color: red;'>{num}</span> "
        elif float(num) == max_num:
            highlighted_sequence += f"<span style='color: blue;'>{num}</span> "
        else:
            highlighted_sequence += f"{num} "
    return highlighted_sequence

if __name__ == '__main__':
    form = cgi.FieldStorage()
    sequence = form.getfirst("sequence", "")

    min_num, max_num = find_min_max(sequence)
    highlighted_sequence = highlight_min_max(sequence, min_num, max_num)
    with open("result.html", encoding="utf-8") as f:
        page = Template(f.read()).substitute(sequence=sequence,
                                             min_num=min_num,
                                             max_num=max_num,
                                             highlighted_sequence=highlighted_sequence)
    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
