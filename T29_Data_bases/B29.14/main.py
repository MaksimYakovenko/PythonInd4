import os
import sqlite3

db_filename = "receipts.db"

def create_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE foods (
            food_id INTEGER NOT NULL, 
            name TEXT,
            PRIMARY KEY (food_id AUTOINCREMENT)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE receipts (
            receipt_id INTEGER NOT NULL,
            food_id INTEGER,
            description TEXT,
            PRIMARY KEY (receipt_id AUTOINCREMENT),
            FOREIGN KEY (food_id)
                REFERENCES foods (food_id)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE ingredients (
            ingredient_id INTEGER NOT NULL,
            name TEXT, 
            PRIMARY KEY (ingredient_id AUTOINCREMENT)
        );
        """
    )

    cursor.execute(
        """ 
        CREATE TABLE receipt_items(
            receipt_id INTEGER NOT NULL,
            ingredient_id INTEGER,
            quantity INTEGER NOT NULL,
            units TEXT,
            FOREIGN KEY (receipt_id)
                REFERENCES receipts (receipt_id),
            FOREIGN KEY (ingredient_id)
                REFERENCES ingredients (ingredient_id)
        );
        """
    )

    conn.commit()
    conn.close()


def add_food(food_name):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO foods (
            name
        ) 
        VALUES (?);
        """,
        (food_name, )
    )
    inserted_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return inserted_id


def add_receipt(food_id, description, ingredients: dict):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO receipts (
            description,
            food_id
        ) 
        VALUES (?, ?);
        """,
        (description, food_id)
    )
    receipt_id = cursor.lastrowid

    for ingr_id, data in ingredients.items():
        cursor.execute(
            """
            INSERT INTO receipt_items (
                ingredient_id,
                receipt_id,
                quantity,
                units 
            )
            VALUES (?, ?, ?, ?);
            """,
            (ingr_id, receipt_id, *data)
        )

    inserted_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return inserted_id


def add_ingredient(name):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ingredients (
            name        
        )
        VALUES (?);
        """,
        (name, )
    )

    inserted_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return inserted_id


def search_receipt(food_name):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT receipts.receipt_id, receipts.description 
            FROM receipts, foods 
            WHERE foods.name = (?) 
        """,
        (food_name, )
    )
    receipts_ids = cursor.fetchall()

    for row in receipts_ids:
        receipt_id = row[0]
        desc = row[1]

        cursor.execute(
            """
            SELECT * FROM receipt_items
            WHERE receipt_id = (?)
            """,
            (receipt_id, )
        )
        ingrs = cursor.fetchall()

        print("Receipt", receipt_id)
        print("Ingredients:")
        for ingr in ingrs:
            cursor.execute("SELECT name FROM ingredients "
                           "WHERE ingredient_id = (?)", (ingr[1], ))
            ingr_name = cursor.fetchall()[0][0]
            print(ingr_name, '-', *ingr[2:])
        print("Description:", desc)

    conn.close()


if __name__ == '__main__':
    create_db()
    water_id = add_ingredient("Вода")
    pork_id = add_ingredient("Свинина")
    potato_id = add_ingredient("Картопля")
    beet_id = add_ingredient("Буряк")
    carrot_id = add_ingredient("Морква")
    borsch_id = add_food("Борщ")
    salt_id = add_ingredient("Сіль")
    description = """Сначала варим бульон. Добавляем мясо и ставим на средний огонь.
     Перед закипанием снимаем пену. Как только бульон закипит, накрываем крышкой
     и варим на медленном огне час-полтора.На среднем огне в сковороде разогреваем
     растительное масло, высыпаем туда лук и морковь, жарим 5 минут. Затем 
     добавляем свеклу (его можно посыпать лимонной кислотой или сбрызнуть 
     соком свежего лимона – так борщ будет по-настоящему красным). Жарим овощи
     еще 5 минут, добавляем томатную пасту, перемешиваем и жарим все еще 5-7 
     минут. Из бульона вынимаем мясо и, пока оно остывает, бросаем в бульон 
     нашинкованную капусту. Через 5-10 минут добавляем нарезанный соломкой 
     картофель. Отделяем мясо от кости и нарезаем кубиками. Возвращаем мясо 
     в борщ, солим его и добавляем зажарку. Перемешиваем борщ, кладем лавровый
     лист и мелко порубленную зелень, накрываем крышкой и варим все еще 5-7 
     минут."""
    ingredients = {
        water_id: (1.5, 'л.'),
        pork_id: (400, 'г.'),
        potato_id: (4, 'шт.'),
        beet_id: (2, 'шт.'),
        carrot_id: (1, 'шт.'),
        salt_id: (1, 'щепотка')

    }
    add_receipt(borsch_id, description, ingredients)
    search_receipt("Борщ")
