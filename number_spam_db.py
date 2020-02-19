import sqlite3
import datetime
import datetime

number_spam_go = 0
id_spam_go = 0
arg = 1

def bd_numbers(phone, id_sp):
    if phone != 0:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        purchases = (None, id_sp, phone, datetime.datetime.now())
        c.execute('INSERT INTO num_spam VALUES (?,?,?,?)', purchases)
        conn.commit()
        conn.close()


def number_spam_proces():
    global number_spam_go, id_spam_go
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT number FROM num_spam;')
    number_spam_go = c.fetchone()[0]
    print("num sp", number_spam_go)
    c.execute('SELECT id_spamer FROM num_spam;')
    id_spam_go = c.fetchone()[0]
    c.execute('DELETE FROM num_spam WHERE number = ?;', [number_spam_go])
    conn.commit()
    conn.close()