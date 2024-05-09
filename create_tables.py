# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 22:36:44 2024

@author: stace
"""

import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

#cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()

connection.close()