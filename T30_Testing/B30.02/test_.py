from app import *
import unittest
import sqlite3
import re
import os
from test.test_wsgiref import run_amock


class TestPassenger(unittest.TestCase):
    def test_01_get_ticket_price(self):
        i = Passenger('Іванов', 'Іван', 'Іванович', 'Місто1', 'Місто2')
        p = Passenger('Петренко', 'Петро', 'Петрович', 'Місто3', 'Місто4')
        a = Passenger('Антонов', 'Антон', 'Антонович', 'Місто5', 'Місто6')
        result1 = i.get_ticket_price(42)
        result2 = p.get_ticket_price(56)
        result3 = a.get_ticket_price(100)
        self.assertIsInstance(result1, int)
        self.assertEqual(result1, 315)
        self.assertEqual(result2, 420)
        self.assertEqual(result3, 750)

    def test_02_get_passengers(self):
        expected_result = [
            'Іванов Іван Іванович',
            'Петренко Петро Петрович',
            'Антонов Антон Антонович',
        ]
        result = get_passengers()
        self.assertIsInstance(result, list)
        self.assertIsNotNone(result)
        self.assertListEqual(expected_result, result)
        self.assertCountEqual(expected_result, result)


    def test_03_get_routes(self):
        expected_result = [
            'Місто1 Місто2 42',
            'Місто3 Місто4 56',
            'Місто5 Місто6 100'
        ]
        result = get_routes()
        self.assertIsInstance(result, list)
        self.assertListEqual(expected_result, result)
        self.assertCountEqual(expected_result, result)

def get_status(response):
    return re.search(r"(?P<STATUS>\d{3} .+?)\n", response).group("STATUS").rstrip()


class TestPassengerResponse(unittest.TestCase):
    def test_04_correct_path_status(self):
        request = b'GET / HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        status = get_status(response)
        self.assertEqual('200 OK', status)

    def test_05_incorrect_path_status(self):
        request = b'GET /incorrect/path HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        status = get_status(response)
        self.assertEqual('404 Page not found', status)


