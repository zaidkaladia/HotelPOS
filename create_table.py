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
    primary_person_name TEXT ,
    primary_person_gender TEXT CHECK(primary_person_gender IN ('Male', 'Female', 'Other')),
    primary_person_mobile TEXT  ,
    alternate_number TEXT,
    primary_person_address TEXT ,
    primary_person_nationality TEXT ,
    primary_person_id_type TEXT CHECK(primary_person_id_type IN ('Aadhar Card', 'Passport', 'Driving License', 'PAN Card', 'Voter ID Card')),
    primary_person_id_number TEXT,
    secondary_person_name TEXT NULL,
    secondary_person_gender TEXT NULL CHECK (secondary_person_gender IS NULL OR secondary_person_gender IN ('Male', 'Female', 'Other')),
    secondary_person_id_type TEXT NULL CHECK (secondary_person_id_type IS NULL OR secondary_person_id_type IN ('Aadhar Card', 'Passport', 'Driving License', 'PAN Card', 'Voter ID Card')),
    secondary_person_id_number TEXT NULL,
    no_of_adults INTEGER,
    no_of_children INTEGER,
    no_of_extra_bed INTEGER,
    room_no TEXT ,
    check_in DATETIME,
    check_out DATETIME,
    bed_type TEXT  CHECK(bed_type IN ('Single', 'Double')),
    room_type TEXT CHECK(room_type IN ('AC', 'Non AC')),
    booking_type TEXT CHECK(booking_type IN ('Walk In', 'Online')),
    no_of_nights INTEGER,
    tour_type TEXT  CHECK(tour_type IN ('Personal', 'Business')),
    company_name TEXT,
    company_address TEXT,
    gst TEXT,
    payment_method TEXT ,
    total_fare REAL  CHECK(total_fare >= 0),
    invoice_date DATE ,
    invoice_no INTEGER UNIQUE
)
''')
print("Created table successfully!")

conn.close()
