import sqlite3
import time

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create proxy table
    c.execute('''
        CREATE TABLE IF NOT EXISTS proxies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proxy_ip TEXT UNIQUE,
            added_time TEXT
        )
    ''')

    # Create request session table
    c.execute('''
        CREATE TABLE IF NOT EXISTS request_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            total_requests INTEGER,
            timestamp TEXT,
            success INTEGER,
            fail INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def save_proxy(proxy_ip):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO proxies (proxy_ip, added_time) VALUES (?, ?)',
                  (proxy_ip, time.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicate proxies
    conn.close()

def get_all_proxies():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT proxy_ip FROM proxies')
    proxies = [row[0] for row in c.fetchall()]
    conn.close()
    return proxies

def delete_proxy(proxy_ip):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM proxies WHERE proxy_ip = ?', (proxy_ip,))
    conn.commit()
    conn.close()

def save_result(url, total_requests, success, fail):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO request_sessions (url, total_requests, timestamp, success, fail)
        VALUES (?, ?, ?, ?, ?)
    ''', (url, total_requests, time.strftime('%Y-%m-%d %H:%M:%S'), success, fail))
    conn.commit()
    conn.close()
