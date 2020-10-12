#!usr/bin/python3
import sqlite3

"""
    Create a database
"""
cur = sqlite3.connect("card.s3db")
cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id integer,
                number text,
                pin text,
                balance integer default 0
            )""")

cur.commit()
