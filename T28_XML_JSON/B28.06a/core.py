import json

FEE = 7.5

class Passenger:
    def __init__(self, name, departure, arrival):
        self.name = name
        self.departure = departure
        self.arrival = arrival

    def get_ticket_price(self):
        with open('./data/routes.json', 'r+') as f:
            routes = json.load(f)
            routes = [r for r in routes if r['departure'] == self.departure and r['arrival'] == self.arrival]
        price = int(routes[0]['distance']) * FEE
        price = int(price) if price % 1 == 0 else price
        with open('./data/results.json', 'r+') as f:
            txt = f.read()
            results = json.loads(txt if txt else '[]')
            results.append({
                'name': self.name,
                'departure': self.departure,
                'arrival': self.arrival,
                'price': price
            })
            f.seek(0)
            f.truncate()
            json.dump(results, f, indent=2, ensure_ascii=False)
        return price


def save_route(departure, arrival, distance):
    with open('./data/routes.json', 'r+') as f:
        txt = f.read()
        routes = json.loads(txt if txt else '[]')
        routes = [r for r in routes if r['departure'] != departure or r['arrival'] != arrival]
        routes.append({
            'departure': departure,
            'arrival': arrival,
            'distance': distance
        })
        f.seek(0)
        f.truncate()
        json.dump(routes, f, indent=2, ensure_ascii=False)


def save_passenger(last_name, name, middle_name):
    with open('./data/passengers.json', 'r+') as f:
        txt = f.read()
        passengers = json.loads(txt if txt else '[]')
        passengers = [p for p in passengers if p['last_name'] != last_name
                      or p['name'] != name
                      or p['middle_name'] != middle_name]
        passengers.append({
            'last_name': last_name,
            'name': name,
            'middle_name': middle_name,
        })
        f.seek(0)
        f.truncate()
        json.dump(passengers, f, indent=2, ensure_ascii=False)
