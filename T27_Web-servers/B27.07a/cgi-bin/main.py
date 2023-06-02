import cgi
from string import Template


def compute_scalar_product(vector1, vector2):
    if len(vector1) != len(vector2):
        return None

    scalar_product = sum(x * y for x, y in zip(vector1, vector2))
    return scalar_product


if __name__ == '__main__':
    form = cgi.FieldStorage()
    vector1 = form.getfirst("vector1", "")
    vector2 = form.getfirst("vector2", "")
    try:
        vector1 = [float(x) for x in vector1.split()]
        vector2 = [float(x) for x in vector2.split()]
    except ValueError:
        result = "Помилка: Некоректні дані"
    else:
        scalar_product = compute_scalar_product(vector1, vector2)
        if scalar_product is not None:
            result = f"Скалярний добуток векторів: {scalar_product}"
        else:
            result = "Помилка: Розміри векторів не співпадають"

    with open("result.html", "r", encoding="utf-8") as file:
        page = Template(file.read()).substitute(result=result)


    import os

    if os.name == "nt":
        import sys, codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    print("Content-type: text/html charset=utf-8\n")
    print(page)
