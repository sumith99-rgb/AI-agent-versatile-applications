import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "liftguard.db")

class MemoryManager:

    def __init__(self):
        # Ensure database is initialized
        if not os.path.exists(DB_PATH):
            from database.schema import init_db
            init_db()

    def _get_connection(self):
        return sqlite3.connect(DB_PATH)

    # -------------------------
    # USER MEMORY
    # -------------------------

    def set_user(self, key, value):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_info (key, value) 
                VALUES (?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            ''', (key, str(value)))
            conn.commit()

    def get_user(self, key):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_info WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_all_user_info(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM user_info')
            return {row[0]: row[1] for row in cursor.fetchall()}

    # -------------------------
    # PREFERENCES
    # -------------------------

    def set_preference(self, key, value):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO preferences (key, value) 
                VALUES (?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            ''', (key, str(value)))
            conn.commit()

    def get_preference(self, key):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    # -------------------------
    # COMPANY
    # -------------------------

    def set_company(self, key, value):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO company (key, value) 
                VALUES (?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            ''', (key, str(value)))
            conn.commit()

    def get_company(self, key):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM company WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    # -------------------------
    # CONVERSATION
    # -------------------------

    def add_message(self, role, message):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversation (role, message) 
                VALUES (?, ?)
            ''', (role, message))
            conn.commit()

    def get_conversation(self, limit=10):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, message FROM conversation 
                ORDER BY id DESC LIMIT ?
            ''', (limit,))
            # Fetch and reverse to maintain chronological order
            rows = cursor.fetchall()
            return [{"role": row[0], "message": row[1]} for row in reversed(rows)]

    def clear_conversation(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM conversation')
            conn.commit()

    # -------------------------
    # TICKETS
    # -------------------------

    def add_ticket(self, ticket):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tickets (ticket_data) 
                VALUES (?)
            ''', (json.dumps(ticket),))
            conn.commit()

    def get_tickets(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ticket_data FROM tickets')
            return [json.loads(row[0]) for row in cursor.fetchall()]

    # -------------------------
    # EMAILS
    # -------------------------

    def add_email(self, recipient, subject, body):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO emails (recipient, subject, body) 
                VALUES (?, ?, ?)
            ''', (recipient, subject, body))
            conn.commit()

    # -------------------------
    # WHATSAPP MESSAGES
    # -------------------------

    def add_whatsapp_message(self, recipient, message):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO whatsapp_messages (recipient, message) 
                VALUES (?, ?)
            ''', (recipient, message))
            conn.commit()