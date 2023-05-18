import os.path
import sqlite3

db_filename = "suppliers.db"

def create_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """
        CREATE TABLE "suppliers" (
         "id"	INTEGER NOT NULL,
         "name"	TEXT NOT NULL,
         "contact_info"	TEXT NOT NULL,
         PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "products" (
         "id"	INTEGER NOT NULL,
         "name"	TEXT NOT NULL,
         "price"	REAL NOT NULL,
         PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE "supplier_products" (
         "supplier_id"	INTEGER,
         "product_id"	INTEGER,
         FOREIGN KEY("supplier_id") REFERENCES "suppliers"("id"),
         FOREIGN KEY("product_id") REFERENCES "products"("id")
        );
        """
    )

def create_supplier(name, contact_info):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO suppliers (name, contact_info) VALUES (?, ?);""",
        (name, contact_info)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def create_product(name, price):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO products (name, price) VALUES (?, ?);""",
        (name, price)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def add_supplier_product(supplier_id, product_id):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO supplier_products VALUES (?, ?);""",
        (supplier_id, product_id)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def find_suppliers_by_product(product_name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT suppliers.name, suppliers.contact_info FROM suppliers
          JOIN supplier_products ON suppliers.id = supplier_products.supplier_id
          JOIN products ON supplier_products.product_id = products.id WHERE 
          products.name = ?""",
        (product_name, )
    )
    suppliers = curs.fetchall()
    conn.commit()
    conn.close()
    return ", ".join(str(e) for e in suppliers[0])

def find_products_by_supplier(supplier_name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT products.name, products.price FROM products
         JOIN supplier_products ON products.id = supplier_products.product_id
          JOIN suppliers ON supplier_products.supplier_id = suppliers.id 
          WHERE suppliers.name = ?;""",
        (supplier_name, )
    )
    products = curs.fetchall()
    conn.commit()
    conn.close()
    return ", ".join(str(e) for e in products[0])


if __name__ == '__main__':
    create_db()
    supplier1_id = create_supplier("Іванов", "+38123123213")
    supplier2_id = create_supplier("Петров", "+38335353535")

    product1_id = create_product("Товар1", 250)
    product2_id = create_product("Товар2", 300)

    supplier_product_1 = add_supplier_product(supplier1_id, product1_id)
    supplier_product_2 = add_supplier_product(supplier2_id, product2_id)

    print(find_products_by_supplier("Іванов"))
    print(find_products_by_supplier("Петров"))
    print(find_suppliers_by_product("Товар1"))
    print(find_suppliers_by_product("Товар2"))
