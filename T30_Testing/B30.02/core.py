import sqlite3

FEE = 7.5
DB_PATH = 'data/data.db'



class Passenger:
    def __init__(self, last_name, name, middle_name, departure, arrival):
        self.distance = None
        self.last_name = last_name
        self.name = name
        self.middle_name = middle_name
        self.departure = departure
        self.arrival = arrival

    def get_ticket_price(self, distance):
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        query = """
        SELECT distance FROM routes
        WHERE departure=? AND arrival=?;"""
        curs.execute(query, (self.departure, self.arrival))
        self.distance = curs.fetchone()[0]
        price = 0
        if distance is not None:
            price = FEE * self.distance
            price = int(price) if price % 1 == 0 else price
        conn.close()
        return price

    @staticmethod
    def add_passenger(last_name, name, middle_name):
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.execute(
            """
            INSERT INTO passengers (last_name, name, middle_name) VALUES (?, ?, ?);
            """, (last_name, name, middle_name)
        )
        inserted_id = curs.lastrowid
        conn.commit()
        conn.close()
        return inserted_id

class DeletePassenger:
    def __init__(self, p_id):
        self.p_id = p_id

    @staticmethod
    def delete_passenger(p_id):
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.execute(
            """DELETE FROM passengers WHERE p_id=?""",
            (p_id, )
        )
        conn.commit()
        conn.close()

class UpdatePassenger:
    def __init__(self, p_id, last_name, name, middle_name):
        self.p_id = p_id
        self.last_name = last_name
        self.name = name
        self.middle_name = middle_name

    def update_passenger(self):
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.execute(
            """UPDATE passengers SET last_name=?, name=?, middle_name=? 
            WHERE p_id=?;""",
            (self.last_name, self.name, self.middle_name, self.p_id)
        )
        conn.commit()
        conn.close()

class Route:
    def __init__(self, departure, arrival, distance):
        self.departure = departure
        self.arrival = arrival
        self.distance = distance

    @staticmethod
    def add_route(departure, arrival, distance):
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.execute(
            """INSERT INTO "routes" VALUES (?, ?, ?);""",
            (departure, arrival, distance)
        )
        conn.commit()
        conn.close()



def get_passengers():
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    curs.execute('SELECT * FROM passengers;')
    res = []
    passengers = curs.fetchall()
    for passenger in passengers:
        res.append(f'{passenger[1]} {passenger[2]} {passenger[3]}')
    conn.commit()
    conn.close()
    return res




def get_routes():
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    curs.execute('SELECT * FROM routes;')
    res = []
    routes = curs.fetchall()
    for route in routes:
        res.append(f'{route[0]} {route[1]} {route[2]}')
    conn.commit()
    conn.close()
    return res

def get_passenger_id():
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    curs.execute('SELECT p_id FROM passengers;')
    res = []
    p_ids = curs.fetchall()
    for p_id in p_ids:
        res.append(f'{p_id[0]}')
    conn.commit()
    conn.close()
    return res

# print(get_passenger_id())