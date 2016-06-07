# coding=utf-8
import sqlite3
import os

is_create_flag = not os.path.exists('bioinfo.db')

conn = sqlite3.connect('bioinfo.db')
c = conn.cursor()

if is_create_flag:
    c.execute('''
    CREATE TABLE user (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username text NOT NULL,
      password text NOT NULL,
      is_admin INTEGER DEFAULT 0
    )
    ''')
    c.execute('''
    CREATE TABLE enzyme (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      uid INTEGER NOT NULL,
      name TEXT NOT NULL,
      site TEXT,
      FOREIGN KEY (uid) REFERENCES user(id)
    )
    ''')
    c.execute('''
    CREATE TABLE gene (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      uid INTEGER NOT NULL,
      sequence TEXT NOT NULL,
      FOREIGN KEY (uid) REFERENCES user(id)
    )
    ''')

    c.execute('''
    CREATE TABLE enzyme_gene (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      gid INTEGER NOT NULL,
      eid INTEGER NOT NULL,
      FOREIGN KEY (gid) REFERENCES gene(id),
      FOREIGN KEY (eid) REFERENCES enzyme(id)
    )
    ''')

    c.execute('INSERT INTO user (username, password, is_admin) VALUES (\'kath\', \'admin\', 1)')
    conn.commit()
