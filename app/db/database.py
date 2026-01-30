import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant TEXT,
            date TEXT,
            total REAL,
            file TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_expense(merchant, date, total, file):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (merchant, date, total, file)
        VALUES (?, ?, ?, ?)
    """, (merchant, date, total, file))

    conn.commit()
    conn.close()


def get_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT merchant, date, total, file FROM expenses ORDER BY id DESC")

    rows = cursor.fetchall()

    conn.close()

    expenses = []

    for row in rows:
        expenses.append({
            "merchant": row[0],
            "date": row[1],
            "total": row[2],
            "file": row[3]
        })

    return expenses
