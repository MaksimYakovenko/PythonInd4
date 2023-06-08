import os.path
import sqlite3

db_filename = "communal_payments.db"

def create_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE payment_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
    )
    curs.execute(
        """
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            payment_type_id INTEGER NOT NULL,
            bill_date TEXT NOT NULL,
            bill_amount REAL NOT NULL,
            payment_date TEXT,
            payment_amount REAL,
            FOREIGN KEY (company_id) REFERENCES companies(id),
            FOREIGN KEY (payment_type_id) REFERENCES payment_types(id)
        );
        """
    )
    conn.commit()
    conn.close()

def add_company(name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO companies (name) VALUES (?)""",
        (name,)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def add_payment_type(name):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO payment_types (name) VALUES (?)""",
        (name,)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def add_payment(company_id, payment_type_id, bill_date, bill_amount, payment_date=None, payment_amount=None):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """INSERT INTO payments (company_id, payment_type_id, bill_date, bill_amount, payment_date, payment_amount)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (company_id, payment_type_id, bill_date, bill_amount, payment_date, payment_amount)
    )
    conn.commit()
    conn.close()
    return curs.lastrowid

def get_payments_by_month_year(month, year):
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT * FROM payments WHERE strftime('%m', bill_date) = ? AND strftime('%Y', bill_date) = ?""",
        (month, year)
    )
    payments = curs.fetchall()
    conn.close()
    return payments

def get_total_bill_amount():
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT SUM(bill_amount) FROM payments"""
    )
    total_amount = curs.fetchone()[0]
    conn.close()
    return total_amount

def get_total_payment_amount():
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    curs.execute(
        """SELECT SUM(payment_amount) FROM payments"""
    )
    total_amount = curs.fetchone()[0]
    conn.close()
    return total_amount

if __name__ == '__main__':
    create_db()

    company1_id = add_company("Company A")
    company2_id = add_company("Company B")

    payment_type1_id = add_payment_type("Water")
    payment_type2_id = add_payment_type("Electricity")

    add_payment(company1_id, payment_type1_id, "2023-05-01", 10.0,
                "2023-05-10", 50.0)
    add_payment(company2_id, payment_type2_id, "2023-05-02", 100.0, "2023-05-11", 100.0)

    payments = get_payments_by_month_year("05", "2023")
    print("Payments for May 2023:")
    for payment in payments:
        print(payment)

    total_bill_amount = get_total_bill_amount()
    print("Total bill amount:", total_bill_amount)

    total_payment_amount = get_total_payment_amount()
    print("Total payment amount:", total_payment_amount)
