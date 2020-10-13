#!usr/bin/python3
import sqlite3

"""
    Create a database
"""
con = sqlite3.connect("card.s3db")
cur = con.cursor()



repeat = False
for value in cur.fetchall():
    print(value)
