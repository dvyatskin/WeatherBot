import os
import sqlite3


def one_insert(command, city_name_min):
    conn = sqlite3.connect(os.path.abspath(os.path.join('database', 'db_history')))
    cur = conn.cursor()

    cur.execute("INSERT INTO history (command, city) VALUES ('%s', '%s')" % (command, city_name_min))
    conn.commit()
    cur.close()
    conn.close()