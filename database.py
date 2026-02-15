import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='urls.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_url(self, short_code, original_url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
            (short_code, original_url)
        )
        conn.commit()
        conn.close()

    def get_url(self, short_code):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT original_url FROM urls WHERE short_code = ?',
            (short_code,)
        )
        result = cursor.fetchone()
        conn.close()
        return result['original_url'] if result else None

    def increment_clicks(self, short_code):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?',
            (short_code,)
        )
        conn.commit()
        conn.close()

    def get_stats(self, short_code):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT short_code, original_url, clicks, created_at FROM urls WHERE short_code = ?',
            (short_code,)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                'short_code': result['short_code'],
                'original_url': result['original_url'],
                'clicks': result['clicks'],
                'created_at': result['created_at']
            }
        return None
