from main import *
import unittest
import sqlite3
import re
from test.test_wsgiref import run_amock


class TestDifference(unittest.TestCase):

    def test_01_difference(self):
        """Тест, який перевіряє правильність обчислення різниці між рядками
        string1 і string2:"""
        string1 = "білий чорний"
        string2 = "чорний"
        value = difference(string1, string2)
        expected_result = "білий"
        self.assertEqual(value, expected_result)


    def test_02_difference(self):
        """Тест, який перевіряє обробку пустих рядків string1 і string2  на
        правильність:"""
        string1 = ""
        string2 = ""
        value = difference(string1, string2)
        expected_result = ""
        self.assertEqual(value, expected_result)


    def test_03_difference(self):
        """Тест, який перевіряє випадок, коли string1 і string2 однакові: """
        string1 = "білий чорний"
        string2 = "білий чорний"
        value = difference(string1, string2)
        expected_result = ""
        self.assertEqual(value, expected_result)


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
