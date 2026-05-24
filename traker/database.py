import sqlite3

def create_connection():
    conn = sqlite3.connect("finance.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def add_transaction(date, description, amount, type, category):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO transactions (date, description, amount, type, category)
        VALUES (?, ?, ?, ?, ?)
    """, (date, description, amount, type, category))
    
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_total_by_type(type):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(amount) FROM transactions WHERE type = ?
    """, (type,))
    
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0

def get_spending_by_category():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return rows