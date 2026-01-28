import sqlite3
import datetime
import os

DB_NAME = '/tmp/obala_analytics.db' if os.environ.get('VERCEL') else 'obala_analytics.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS visits 
                     (id INTEGER PRIMARY KEY, timestamp TEXT, user_agent TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS translations 
                     (id INTEGER PRIMARY KEY, timestamp TEXT, direction TEXT, variant TEXT, original_length INTEGER)''')
        conn.commit()
        conn.close()

def log_visit(user_agent):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO visits (timestamp, user_agent) VALUES (?, ?)", 
                  (datetime.datetime.now().isoformat(), user_agent))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Log Error: {e}")

def log_translation(direction, variant, text_len):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO translations (timestamp, direction, variant, original_length) VALUES (?, ?, ?, ?)", 
                  (datetime.datetime.now().isoformat(), direction, variant, text_len))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Log Error: {e}")
