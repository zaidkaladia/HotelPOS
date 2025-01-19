# Author: Clinton Daniel, University of South Florida
# Date: 4/4/2023
# Description: This python script assumes that you already have
# a database.db file at the root of your workspace.
# This python script will CREATE a table called students 
# in the database.db using SQLite3 which will be used
# to store the data collected by the forms in this app
# Execute this python script before testing or editing this app code. 
# Open a python terminal and execute this script:
# python create_table.py

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('''
CREATE TABLE HotelManagement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    primary_person_name TEXT NOT NULL,
    primary_person_gender TEXT CHECK(primary_person_gender IN ('Male', 'Female', 'Other')),
    primary_person_mobile TEXT NOT NULL ,
    alternate_number TEXT,
    primary_person_address TEXT ,
    primary_person_nationality TEXT NOT NULL,
    primary_person_id_type TEXT NOT NULL CHECK(primary_person_id_type IN ('Aadhar Card', 'Passport', 'Driving License', 'PAN Card', 'Voter ID Card')),
    primary_person_id_number TEXT NOT NULL,
    secondary_person_name TEXT,
    secondary_person_gender TEXT CHECK(secondary_person_gender IN ('Male', 'Female', 'Other')),
    secondary_person_id_type TEXT CHECK(secondary_person_id_type IN ('Aadhar Card', 'Passport', 'Driving License', 'PAN Card', 'Voter ID Card')),
    secondary_person_id_number TEXT,
    room_no INTEGER NOT NULL,
    room_name TEXT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE,
    bed_type TEXT NOT NULL CHECK(bed_type IN ('Single', 'Double')),
    room_type TEXT NOT NULL CHECK(room_type IN ('AC', 'Non AC')),
    no_of_nights INTEGER NOT NULL,
    tour_type TEXT NOT NULL CHECK(tour_type IN ('Personal', 'Business')),
    company_name TEXT,
    gst TEXT,
    payment_method TEXT NOT NULL,
    total_fare REAL NOT NULL CHECK(total_fare >= 0),
    invoice_date DATE NOT NULL,
    invoice_no TEXT NOT NULL UNIQUE
)
''')
print("Created table successfully!")

conn.close()
