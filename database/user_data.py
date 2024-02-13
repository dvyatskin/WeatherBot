import sqlite3

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()


def create_tables(conn, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_temp_range
                      (user_id INTEGER PRIMARY KEY, min_temp REAL, max_temp REAL)''')


def set_temp_range(conn, cursor, user_id, min_temp, max_temp):
    cursor.execute("INSERT OR REPLACE INTO user_temp_range (user_id, min_temp, max_temp) VALUES (?, ?, ?)",
                   (user_id, min_temp, max_temp))
    conn.commit()


def get_temp_range(conn, cursor, user_id):
    cursor.execute("SELECT min_temp, max_temp FROM user_temp_range WHERE user_id=?", (user_id,))
    return cursor.fetchone()
