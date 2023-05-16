import os.path
import sqlite3

db_filename = "trees.db"

def create_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """
        CREATE TABLE "tree_species" (
	        "id"	INTEGER NOT NULL,
	        "name"	TEXT NOT NULL,
	        PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "tree_varieties" (
	        "id"	INTEGER NOT NULL,
            "name"	TEXT NOT NULL,
            "species_id"	INTEGER NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("species_id") REFERENCES "tree_species"("id")
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "trees" (
            "id"	INTEGER NOT NULL,
            "variety_id"	INTEGER NOT NULL,
            "year_planted"	INTEGER NOT NULL,
            "location"	INTEGER NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("variety_id") REFERENCES "tree_varieties"("id")
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "harvest" (
	        "id"	INTEGER NOT NULL,
            "tree_id"	INTEGER NOT NULL,
            "year"	INTEGER NOT NULL,
            "harvest_kg"	REAL NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("tree_id") REFERENCES "trees"("id")
        );
        """
    )
    conn.commit()
    conn.close()

def add_species(name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO tree_species (name) VALUES (?);""",
        (name, )
    )
    species_id = curs.lastrowid
    conn.commit()
    conn.close()
    return species_id

def add_variety(name, species_id):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO tree_varieties (name, species_id) VALUES (?, ?);""",
        (name, species_id)
    )
    variety_id = curs.lastrowid
    conn.commit()
    conn.close()
    return variety_id

def add_tree(variety_id, year_planted, location):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO trees (variety_id, year_planted, location) VALUES (?, ?, ?);""",
        (variety_id, year_planted, location)
    )
    tree_id = curs.lastrowid
    conn.commit()
    conn.close()
    return tree_id

def add_harvest(tree_id, year, harvest_kg):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute("""INSERT INTO harvest (tree_id, year, harvest_kg) VALUES (?, ?, ?);""",
                 (tree_id, year, harvest_kg)
    )
    harvest_id = curs.lastrowid
    conn.commit()
    conn.close()
    return harvest_id

def get_trees_by_species(species_name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT tv.name, t.year_planted, t.location, y.year, y.harvest_kg FROM trees t """
        """JOIN tree_varieties tv ON t.variety_id = tv.id """
        """JOIN tree_species ts ON tv.species_id = ts.id """
        """LEFT JOIN harvest y ON t.id = y.tree_id """
        'WHERE ts.name = ?',
        (species_name,)
    )
    info = curs.fetchall()
    result_string = " ".join(str(e) for e in info[0])
    return result_string

def get_harvest_for_tree(tree_id, start_year, end_year):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute("""SELECT year, harvest_kg FROM harvest """
                    """WHERE tree_id = ? AND year >= ? AND year <= ?""", (tree_id, start_year, end_year))
    info = curs.fetchall()
    result_string = " ".join(str(e) for e in info[0])
    return result_string


if __name__ == '__main__':
    create_db()
    apple_tree_id = add_species("Яблуня")
    apple_tree_variety = add_variety("Білий налив", apple_tree_id)
    tree1_id = add_tree(apple_tree_variety, 2020, "Place1")
    add_harvest(tree1_id, 2022, 15)

    pear_tree_id = add_species("Груша")



    print(get_harvest_for_tree(1, 2020, 2022))
    print(get_trees_by_species("Яблуня"))
