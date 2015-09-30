#!/usr/bin/python3

"""
Scrapes latest data from the MTA Turnstile info 
(http://web.mta.info/developers/turnstile.html)
and dumps it into a given database

Usage: python mta_turnsite_scraper.py <db>
"""

import sqlite3
from util import trace

# Globals
# Columns
COLUMN_HEADERS = "CA,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS".split(',') 
COLUMN_DATATYPES = "TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,DATE,TIME,TEXT,INTEGER,INTEGER".split(',')

# Database
DATABASE = 'test.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

"""
Given a turnstile data file, parse data and dump into database
"""
def file_to_db(filename):

    with open(filename) as f:
        next(f) # skip header
        for line in f:
            add_entry_db(line)
    commit_db()
    return

"""
Commit db entries
"""
def commit_db():
    connection.commit()
    trace('commit db')
    return

"""
Given a line of entry from raw, add that entry to db without commiting
"""
def add_entry_db(line):
    # format values accordingly
    values = []
    count = 0
    for val in line.split(','):
        values.append("'" + val + "'")
    
    values.prepend(None)
    values = tuple(values)
    insert_query = 'INSERT INTO entries VALUES(?)'
    trace(insert_query, values)
    cursor.execute(insert_query, values)
    return

"""
Clear all tables
"""
def clear_db():
    confirm = input('Sure you wanna drop all tables?')
    if confirm is 'y':
        cursor.execute('DROP TABLE entries')
        commit_db()

"""
Set up database
"""
def init_db():
    # create headers for entries 

    header_and_datatypes = "id INTEGER PRIMARY KEY AUTOINCREMENT,  " + ", ".join([COLUMN_HEADERS[i] + ' ' + COLUMN_DATATYPES[i] for i in range(len(COLUMN_HEADERS))])
    create_query =  'CREATE TABLE IF NOT EXISTS entries (' + header_and_datatypes + ')'
    
    # create 'entries' table
    cursor.execute(create_query)
    return

def test():
    init_db()
    trace(cursor)
    add_entry_db('A002,R051,02-00-00,LEXINGTON AVE,NQR456,BMT,09/19/2015,00:00:00,REGULAR,0005317608,0001797091')
    commit_db()
    assert len(cursor.execute('SELECT * FROM entries WHERE CA=?', ('A002',)).fetchall()) == 1
    trace('tests pass')
