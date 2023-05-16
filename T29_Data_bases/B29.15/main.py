import os.path
import sqlite3

db_filename = "real_estate.db"

def create_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """
        CREATE TABLE "real_estate" (
         "id"	INTEGER NOT NULL,
         "type"	TEXT NOT NULL,
         "address"	TEXT NOT NULL,
         "area"	REAL NOT NULL,
         "rooms"	INTEGER NOT NULL,
         PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "rooms" (
         "id"	INTEGER NOT NULL,
         "estate_id"	INTEGER NOT NULL,
         "purpose"	TEXT NOT NULL,
         "area"	REAL NOT NULL,
         FOREIGN KEY("estate_id") REFERENCES "real_estate"("id"),
         PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )
def add_real_estate(type, address, area, rooms):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO real_estate (type, address, area, rooms) VALUES (?, ?, ?, ?)""",
        (type, address, area, rooms)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def add_room(estate_id, purpose, area):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO rooms (estate_id, purpose, area) VALUES (?, ?, ?)""",
        (estate_id, purpose, area)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def get_real_estate_by_type_and_area(type, min_area):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT * FROM real_estate WHERE type=? AND area>=?""",
        (type, min_area))
    estates = curs.fetchall()
    for estate in estates:
        curs.execute("""SELECT * FROM rooms WHERE estate_id=?""",
                     (estate[0], ))
        rooms = curs.fetchall()
        estate += (rooms, )
    result_string = ", ".join(str(e) for e in estates[0])
    return result_string

if __name__ == '__main__':
    create_db()
    estate1_id = add_real_estate("Квартира", "вул. Петра Запорожця 7", 70, 3)
    add_room(estate1_id, "Спальня", 20)
    add_room(estate1_id, "Кухня", 15)
    add_room(estate1_id, "Ванна", 10)

    estate2_id = add_real_estate('Будинок', 'вул. Київська, 14', 200, 5)
    add_room(estate2_id, 'Спальня', 25)
    add_room(estate2_id, 'Вітальня', 40)
    add_room(estate2_id, 'Кухня', 20)

    print(get_real_estate_by_type_and_area("Квартира", 70))
    print(get_real_estate_by_type_and_area("Будинок", 200))
