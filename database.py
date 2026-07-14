import sqlite3

# Connect to database
connection = sqlite3.connect("hospital.db")

cursor = connection.cursor()

# ==============================
# ADMIN TABLE
# ==============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(

    username TEXT PRIMARY KEY,

    password TEXT NOT NULL

)
""")

# ==============================
# DOCTOR TABLE
# ==============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors(

    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,

    doctor_name TEXT NOT NULL,

    specialization TEXT NOT NULL,

    phone TEXT,

    email TEXT

)
""")

# ==============================
# PATIENT TABLE
# ==============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(

    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_name TEXT NOT NULL,

    age INTEGER NOT NULL,

    gender TEXT NOT NULL,

    phone TEXT NOT NULL,

    disease TEXT NOT NULL

)
""")

# ==============================
# APPOINTMENT TABLE
# ==============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(

    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER,

    doctor_id INTEGER,

    appointment_date TEXT,

    appointment_time TEXT,

    status TEXT,

    FOREIGN KEY(patient_id) REFERENCES patients(patient_id),

    FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)

)
""")

# ==============================
# DEFAULT ADMIN
# ==============================

cursor.execute("""
INSERT OR IGNORE INTO admin(username,password)
VALUES('admin','Admin@123')
""")
connection.commit()
connection.close()

print("Hospital Database Created Successfully!")