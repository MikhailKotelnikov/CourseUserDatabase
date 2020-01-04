# We're making "course-user" database here (many to many). We're achieving it by adding "member" table. We're reading data from json file.

import sqlite3
import json

connect = sqlite3.connect('courses.sqlite')
cursor = connect.cursor()

cursor.executescript('''
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member;
    DROP TABLE IF EXISTS User;
    
    CREATE TABLE Course(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

    
    CREATE TABLE Member(
        user_id INTEGER,
        course_id INTEGER,
        role INTEGER,
        PRIMARY KEY (user_id, course_id)
    );
    
    CREATE TABLE User(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

''')

# open json file

str_data_from_json = open('courses_data.json').read()

json_data = json.loads(str_data_from_json)

for entry in json_data:
    name = entry[0]
    course_name = entry[1]
    role = entry[2]
    
    cursor.execute('''INSERT OR IGNORE INTO User (name) VALUES (?)''', (name,))
    cursor.execute('''SELECT id FROM User WHERE name = ?''', (name,))
    user_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Course (name) VALUES (?)''', (course_name,))
    cursor.execute('''SELECT id FROM Course WHERE name = ?''', (course_name,))
    course_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)''', (user_id, course_id, role,))
    

connect.commit()