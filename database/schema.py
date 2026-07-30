import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "liftguard.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table (Single user context for now, but storing multiple fields)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Preferences Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Company Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Conversation Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tickets Table (Stored as JSON text for simplicity, or structured columns)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Emails Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject TEXT,
            body TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # WhatsApp Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whatsapp_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Initialized database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
