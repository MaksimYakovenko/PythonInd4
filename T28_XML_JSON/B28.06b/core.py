import xml.etree.ElementTree as ET

FEE = 7.5


class Passenger:
    def __init__(self, name, departure, arrival):
        self.name = name
        self.departure = departure
        self.arrival = arrival

    def get_ticket_price(self):
        route_tree = ET.parse('./data/routes.xml')
        price = None
        for route in route_tree.getroot().findall('route'):
            departure = route.find('departure').text.strip()
            arrival = route.find('arrival').text.strip()
            distance = route.find('distance').text.strip()
            if departure == self.departure and arrival == self.arrival:
                price = int(distance) * FEE
                break
        price = int(price) if price % 1 == 0 else price

        tree = ET.parse('./data/results.xml')
        root = tree.getroot()
        element = ET.fromstring(
            f'<ticket>'
            f'<name>{self.name}</name>'
            f'<departure>{self.departure}</departure>'
            f'<arrival>{self.arrival}</arrival>'
            f'<price>{price}</price>'
            f'</ticket>')
        root.append(element)
        tree.write('./data/results.xml')
        return price


def save_route(departure, arrival, distance):
    tree = ET.parse('./data/routes.xml')
    root = tree.getroot()
    element = ET.fromstring(
        f'<route><departure>{departure}</departure><arrival>{arrival}</arrival><distance>{distance}</distance></route>')
    root.append(element)
    tree.write('./data/routes.xml')


def save_passenger(last_name, name, middle_name):
    tree = ET.parse('./data/passengers.xml')
    root = tree.getroot()
    element = ET.fromstring(f'<passenger>'
                            f'<last_name>{last_name}</last_name>'
                            f'<name>{name}</name>'
                            f'<middle_name>{middle_name}</middle_name>'
                            f'</passenger>')
    root.append(element)
    tree.write('./data/passengers.xml')
