import sqlite3
import telebot
import datetime

baza_viv = ''
time_sms = ''
ver = 0


def reg(chat_id, user_name, full_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    purchases = (chat_id, user_name, full_name, 0, 0)
    c.execute('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


def spam_date(chat_id):
    print(chat_id)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    ad = (datetime.datetime.now(), chat_id)
    c.execute('UPDATE users SET time = ? WHERE chat_id = ?;', ad)
    conn.commit()
    conn.close()


def date_sms_spam(chat_id):
    global time_sms
    global ver
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT pro_ver FROM users WHERE chat_id = ?;', [chat_id])
    ver = c.fetchone()[0]
    c.execute('SELECT time FROM users WHERE chat_id = ?;', [chat_id])
    time_sms = c.fetchone()[0]
    conn.commit()
    conn.close()


def db_info_adm():
    global baza_viv
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users;')
    while c.fetchone() != None:
        print(c.fetchone())
    conn.commit()
    conn.close()

