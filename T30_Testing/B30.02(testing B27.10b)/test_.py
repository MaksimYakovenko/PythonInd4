from main import *
from test.test_wsgiref import run_amock
import re
import unittest

class TestRemoveBrackets(unittest.TestCase):
    """Тест на видалення дужок з рядка, що містить дужки:"""
    def test_01_remove_brackets(self):
        string = "text (text with brackets)"
        value = remove_brackets(string)
        expected_value = "text "
        self.assertEqual(value, expected_value)

    def test_02_remove_brackets(self):
        """Тест на видалення дужок з рядка без дужок:"""
        string = "text without brackets"
        value = remove_brackets(string)
        expected_value = "text without brackets"
        self.assertEqual(value, expected_value)

    def test_03_remove_brackets(self):
        """Тест на видалення дужок з порожнього рядка:"""
        string = ""
        value = remove_brackets(string)
        expected_value = ""
        self.assertEqual(value, expected_value)

def get_status(response):
    """ Повертає http статус відповіді: код і короткий опис"""
    return re.search(r"(?P<STATUS>\d{3} .+?)\n", response).group("STATUS").rstrip()


class TestRemoveBracketsResponse(unittest.TestCase):
    def test_01_correct_path_status(self):
        """ Коректність статусу відповіді при правильному шляху.
            Намагаємося відкрити головну сторінку "/" .
            Очікуємо, що статус відповіді буде "200 OK".
        """
        request = b"GET / HTTP/1.0\n"
        out, err = run_amock(application, request)
        response = str(out, encoding="utf-8")
        status = get_status(response)
        self.assertEqual("200 OK", status)

    def test_02_incorrect_path_status(self):
        """ Коректність статусу відповіді при неправильному шляху.
            Намагаємося відкрити сторінку "/incorrect/path".
            Очікуємо, що статус відповіді буде "404 NOT FOUND".
        """
        request = b'GET /incorrect/path HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding="utf-8")
        status = get_status(response)
        self.assertEqual("404 NOT FOUND", status)
