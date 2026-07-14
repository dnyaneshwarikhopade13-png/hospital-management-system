from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "hospital_management_system"

# -----------------------------
# Login Page
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------
# Login Authentication
# -----------------------------
@app.route("/login", methods=["POST"])
def check_login():

    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (username, password)
    )

    admin = cursor.fetchone()

    connection.close()

    if admin:

        session["admin"] = username

        return redirect("/dashboard")

    return "Invalid Username or Password"


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/")

    return render_template("dashboard.html")

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():

    if "admin" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("add_doctor.html")

    # Get form data
    doctor_name = request.form["doctor_name"]
    specialization = request.form["specialization"]
    phone = request.form["phone"]

    # Validate phone number
    if not phone.isdigit() or len(phone) != 10:
        return "<h2 style='color:red; text-align:center;'>Phone number must contain exactly 10 digits.</h2>"

    email = request.form["email"]

    # Connect to database
    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Insert doctor
    cursor.execute(
        """
        INSERT INTO doctors
        (doctor_name, specialization, phone, email)
        VALUES (?, ?, ?, ?)
        """,
        (doctor_name, specialization, phone, email)
    )

    connection.commit()
    connection.close()

    return render_template(
        "success.html",
        title="✅ Doctor Added Successfully!",
        message="The doctor's information has been saved successfully.",
        add_url="/add_doctor",
        add_button="Add Another Doctor"
    )
@app.route("/view_doctors")
def view_doctors():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM doctors")

    doctors = cursor.fetchall()

    connection.close()

    return render_template(
        "view_doctors.html",
        doctors=doctors
    )

@app.route("/delete_doctor/<int:doctor_id>")
def delete_doctor(doctor_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM doctors WHERE doctor_id=?",
        (doctor_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/view_doctors")
@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor(doctor_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Open Edit Form
    if request.method == "GET":

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id=?",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        connection.close()

        return render_template(
            "edit_doctor.html",
            doctor=doctor
        )

    # Update Doctor Details
    doctor_name = request.form["doctor_name"]
    specialization = request.form["specialization"]
    phone = request.form["phone"]
    email = request.form["email"]

    cursor.execute(
        """
        UPDATE doctors
        SET doctor_name=?,
            specialization=?,
            phone=?,
            email=?
        WHERE doctor_id=?
        """,
        (doctor_name, specialization, phone, email, doctor_id)
    )

    connection.commit()
    connection.close()

    return redirect("/view_doctors")

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():

    if "admin" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("add_patient.html")

    patient_name = request.form["patient_name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]

    if not phone.isdigit() or len(phone) != 10:
        return "<h2 style='color:red; text-align:center;'>Phone number must contain exactly 10 digits.</h2>"

    disease = request.form["disease"]

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
    """
    INSERT INTO patients
    (patient_name, age, gender, phone, disease)
    VALUES (?, ?, ?, ?, ?)
    """,
    (patient_name, age, gender, phone, disease)
)

    connection.commit()
    connection.close()

    return render_template(
        "success.html",
        title="✅ Patient Added Successfully!",
        message="The patient's information has been saved successfully.",
        add_url="/add_patient",
        add_button="Add Another Patient"
    )
@app.route("/view_patients")
def view_patients():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM patients")

    patients = cursor.fetchall()

    connection.close()

    return render_template(
        "view_patients.html",
        patients=patients
    )
@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=?",
        (patient_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/view_patients")

@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Display the edit form
    if request.method == "GET":

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id=?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        connection.close()

        return render_template(
            "edit_patient.html",
            patient=patient
        )

    # Update patient details
    patient_name = request.form["patient_name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    disease = request.form["disease"]

    cursor.execute(
        """
        UPDATE patients
        SET patient_name=?,
            age=?,
            gender=?,
            phone=?,
            disease=?
        WHERE patient_id=?
        """,
        (patient_name, age, gender, phone, disease, patient_id)
    )

    connection.commit()
    connection.close()

    return redirect("/view_patients")

@app.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # -------------------------
    # Open Appointment Page
    # -------------------------
    if request.method == "GET":

        cursor.execute("SELECT doctor_id, doctor_name FROM doctors")
        doctors = cursor.fetchall()

        cursor.execute("SELECT patient_id, patient_name FROM patients")
        patients = cursor.fetchall()

        connection.close()

        return render_template(
            "book_appointment.html",
            doctors=doctors,
            patients=patients
        )

    # -------------------------
    # Save Appointment
    # -------------------------

    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]

    cursor.execute(
        """
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            "Scheduled"
        )
    )

    connection.commit()
    connection.close()

    return render_template(
        "success.html",
        title="✅ Appointment Booked Successfully!",
        message="The appointment has been booked successfully.",
        add_url="/book_appointment",
        add_button="Book Another Appointment"
    )
@app.route("/view_appointments")
def view_appointments():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT

        appointments.appointment_id,

        patients.patient_name,

        doctors.doctor_name,

        appointments.appointment_date,

        appointments.appointment_time,

        appointments.status

    FROM appointments

    JOIN patients
    ON appointments.patient_id = patients.patient_id

    JOIN doctors
    ON appointments.doctor_id = doctors.doctor_id
    """)

    appointments = cursor.fetchall()

    connection.close()

    return render_template(
        "view_appointments.html",
        appointments=appointments
    )
@app.route("/delete_appointment/<int:appointment_id>")
def delete_appointment(appointment_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM appointments WHERE appointment_id=?",
        (appointment_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/view_appointments")    
    # Get Form Data
    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]

    cursor.execute(
        """
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            "Scheduled"
        )
    )

    connection.commit()
    connection.close()

    return render_template(
        "success.html",
        title="✅ Appointment Booked Successfully!",
        message="The appointment has been booked successfully.",
        add_url="/book_appointment",
        add_button="Book Another Appointment"
    )
@app.route("/edit_appointment/<int:appointment_id>", methods=["GET", "POST"])
def edit_appointment(appointment_id):

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # -----------------------
    # Show Edit Form
    # -----------------------
    if request.method == "GET":

        cursor.execute("""
            SELECT
                appointment_id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status
            FROM appointments
            WHERE appointment_id=?
        """, (appointment_id,))

        appointment = cursor.fetchone()

        connection.close()

        return render_template(
            "edit_appointment.html",
            appointment=appointment
        )

    # -----------------------
    # Update Appointment
    # -----------------------

    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    status = request.form["status"]

    cursor.execute("""
        UPDATE appointments
        SET appointment_date=?,
            appointment_time=?,
            status=?
        WHERE appointment_id=?
    """, (
        appointment_date,
        appointment_time,
        status,
        appointment_id
    ))

    connection.commit()
    connection.close()

    return redirect("/view_appointments")

@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    # Total Doctors
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]

    # Total Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    # Total Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    # Scheduled Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='Scheduled'")
    scheduled = cursor.fetchone()[0]

    # Completed Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    # Cancelled Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='Cancelled'")
    cancelled = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "reports.html",
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_appointments=total_appointments,
        scheduled=scheduled,
        completed=completed,
        cancelled=cancelled
    ) 
@app.route("/medicine")
def medicine():

    if "admin" not in session:
        return redirect("/")

    return render_template("medicine.html")

@app.route("/medicine_result", methods=["POST"])
def medicine_result():

    if "admin" not in session:
        return redirect("/")

    disease = request.form["disease"].strip().lower()

    medicines = {

        "fever": [
            "Paracetamol 500 mg",
            "Dolo 650",
            "Crocin"
        ],

        "cold": [
            "Cetirizine",
            "Sinarest",
            "Levocetirizine"
        ],

        "cough": [
            "Benadryl Syrup",
            "Ascoril Syrup",
            "Ambroxol"
        ],

        "diabetes": [
            "Metformin",
            "Glibenclamide",
            "Insulin (Doctor's Advice)"
        ],

        "blood pressure": [
            "Amlodipine",
            "Telmisartan",
            "Losartan"
        ],

        "headache": [
            "Paracetamol",
            "Ibuprofen",
            "Crocin"
        ],

        "stomach pain": [
            "Pantoprazole",
            "Omeprazole",
            "Antacid Syrup"
        ]
    }

    result = medicines.get(
        disease,
        ["No medicine found for this disease."]
    )

    return render_template(
        "medicine_result.html",
        disease=disease.title(),
        medicines=result
    )
@app.route("/billing")
def billing():

    if "admin" not in session:
        return redirect("/")

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute("SELECT patient_id, patient_name FROM patients")
    patients = cursor.fetchall()

    connection.close()

    return render_template(
        "billing.html",
        patients=patients
    )
@app.route("/generate_bill", methods=["POST"])
def generate_bill():

    if "admin" not in session:
        return redirect("/")

    patient_id = request.form["patient_id"]

    consultation = int(request.form["consultation_fee"])

    medicine = int(request.form["medicine_charge"])

    room = int(request.form["room_charge"])

    test = int(request.form["test_charge"])

    total = consultation + medicine + room + test

    connection = sqlite3.connect("hospital.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT patient_name FROM patients WHERE patient_id=?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    connection.close()

    return render_template(

        "bill_result.html",

        patient=patient[0],

        consultation=consultation,

        medicine=medicine,

        room=room,

        test=test,

        total=total

    )
# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)