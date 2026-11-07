# Hospital Management System
# Python + MySQL interface (mysql.connector)
# Tables: doctors, patients, appointments

import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = "admin"      # change to your MySQL password
DATABASE = "hospital"


def connect_database():
    # Create the database (first time) and connect to it
    con = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE)
    con.close()
    con = mysql.connector.connect(host=HOST, user=USER,
                                  password=PASSWORD, database=DATABASE)
    return con


def create_tables(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS doctors (
                    doc_id INT PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    department VARCHAR(30),
                    fees INT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS patients (
                    pat_id INT PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    age INT,
                    gender CHAR(1),
                    phone VARCHAR(10))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS appointments (
                    app_id INT PRIMARY KEY AUTO_INCREMENT,
                    pat_id INT,
                    doc_id INT,
                    app_date DATE,
                    status VARCHAR(10) DEFAULT 'Booked',
                    FOREIGN KEY (pat_id) REFERENCES patients(pat_id),
                    FOREIGN KEY (doc_id) REFERENCES doctors(doc_id))""")

    # Add some doctors the first time so the program can be used at once
    cur.execute("SELECT COUNT(*) FROM doctors")
    if cur.fetchone()[0] == 0:
        doctors = [(101, "Dr. R.K. Sharma", "Cardiology", 800),
                   (102, "Dr. Meena Joshi", "Pediatrics", 500),
                   (103, "Dr. Anil Rawat", "Orthopedics", 600),
                   (104, "Dr. Sunita Bisht", "General", 300),
                   (105, "Dr. Vikas Pant", "Cardiology", 700)]
        cur.executemany("INSERT INTO doctors VALUES (%s, %s, %s, %s)", doctors)
        con.commit()


# ---------------- Doctors ----------------

def add_doctor(con):
    cur = con.cursor()
    doc_id = int(input("Enter Doctor ID: "))
    name = input("Enter Doctor Name: ")
    dept = input("Enter Department: ")
    fees = int(input("Enter Consultation Fees: "))
    cur.execute("INSERT INTO doctors VALUES (%s, %s, %s, %s)",
                (doc_id, name, dept, fees))
    con.commit()
    print("Doctor added successfully!")


def show_doctors(con):
    cur = con.cursor()
    dept = input("Enter Department (press Enter for all): ")
    if dept == "":
        cur.execute("SELECT * FROM doctors ORDER BY department")
    else:
        cur.execute("SELECT * FROM doctors WHERE department = %s", (dept,))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No doctors found.")
        return
    print("%-6s %-20s %-14s %6s" % ("ID", "Name", "Department", "Fees"))
    print("-" * 50)
    for r in rows:
        print("%-6d %-20s %-14s %6d" % r)


# ---------------- Patients ----------------

def add_patient(con):
    cur = con.cursor()
    pat_id = int(input("Enter Patient ID: "))
    name = input("Enter Patient Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender (M/F): ").upper()
    phone = input("Enter Phone Number: ")
    cur.execute("INSERT INTO patients VALUES (%s, %s, %s, %s, %s)",
                (pat_id, name, age, gender, phone))
    con.commit()
    print("Patient registered successfully!")


def search_patient(con):
    cur = con.cursor()
    name = input("Enter name (or part of name) to search: ")
    cur.execute("SELECT * FROM patients WHERE name LIKE %s", ("%" + name + "%",))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No patient found.")
        return
    print("%-6s %-20s %4s %6s %-10s" % ("ID", "Name", "Age", "Gender", "Phone"))
    print("-" * 50)
    for r in rows:
        print("%-6d %-20s %4d %6s %-10s" % r)


# ---------------- Appointments ----------------

def book_appointment(con):
    cur = con.cursor()
    pat_id = int(input("Enter Patient ID: "))
    doc_id = int(input("Enter Doctor ID: "))
    app_date = input("Enter Date (YYYY-MM-DD): ")
    cur.execute("INSERT INTO appointments (pat_id, doc_id, app_date) VALUES (%s, %s, %s)",
                (pat_id, doc_id, app_date))
    con.commit()
    print("Appointment booked! Appointment ID:", cur.lastrowid)


def cancel_appointment(con):
    cur = con.cursor()
    app_id = int(input("Enter Appointment ID to cancel: "))
    cur.execute("UPDATE appointments SET status = 'Cancelled' WHERE app_id = %s", (app_id,))
    con.commit()
    if cur.rowcount > 0:
        print("Appointment", app_id, "cancelled.")
    else:
        print("No appointment found with ID", app_id)


def show_appointments(con):
    cur = con.cursor()
    # JOIN of three tables
    cur.execute("""SELECT a.app_id, p.name, d.name, d.department, a.app_date, a.status
                   FROM appointments a, patients p, doctors d
                   WHERE a.pat_id = p.pat_id AND a.doc_id = d.doc_id
                   ORDER BY a.app_date""")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No appointments found.")
        return
    print("%-4s %-16s %-18s %-12s %-11s %-9s" %
          ("ID", "Patient", "Doctor", "Department", "Date", "Status"))
    print("-" * 75)
    for r in rows:
        print("%-4d %-16s %-18s %-12s %-11s %-9s" %
              (r[0], r[1], r[2], r[3], str(r[4]), r[5]))


# ---------------- Reports ----------------

def reports(con):
    cur = con.cursor()
    print("\n--- Appointments per Department (GROUP BY) ---")
    cur.execute("""SELECT d.department, COUNT(*)
                   FROM appointments a, doctors d
                   WHERE a.doc_id = d.doc_id AND a.status = 'Booked'
                   GROUP BY d.department""")
    for r in cur.fetchall():
        print("%-14s : %d" % r)

    print("\n--- Fees Collected by each Doctor (SUM) ---")
    cur.execute("""SELECT d.name, SUM(d.fees)
                   FROM appointments a, doctors d
                   WHERE a.doc_id = d.doc_id AND a.status = 'Booked'
                   GROUP BY d.name
                   ORDER BY SUM(d.fees) DESC""")
    for r in cur.fetchall():
        print("%-20s : Rs. %d" % (r[0], r[1]))

    print("\n--- Patient Statistics (MIN, MAX, AVG) ---")
    cur.execute("SELECT COUNT(*), MIN(age), MAX(age), AVG(age) FROM patients")
    r = cur.fetchone()
    print("Total Patients:", r[0])
    if r[0] > 0:
        print("Youngest:", r[1], "| Oldest:", r[2], "| Average Age:", round(float(r[3]), 1))


def main():
    try:
        con = connect_database()
    except mysql.connector.Error as e:
        print("Could not connect to MySQL:", e)
        return
    create_tables(con)

    while True:
        print("\n======= HOSPITAL MANAGEMENT SYSTEM =======")
        print("1. Add Doctor")
        print("2. Show Doctors")
        print("3. Register Patient")
        print("4. Search Patient")
        print("5. Book Appointment")
        print("6. Cancel Appointment")
        print("7. Show All Appointments")
        print("8. Reports")
        print("9. Exit")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                add_doctor(con)
            elif choice == "2":
                show_doctors(con)
            elif choice == "3":
                add_patient(con)
            elif choice == "4":
                search_patient(con)
            elif choice == "5":
                book_appointment(con)
            elif choice == "6":
                cancel_appointment(con)
            elif choice == "7":
                show_appointments(con)
            elif choice == "8":
                reports(con)
            elif choice == "9":
                con.close()
                print("Database connection closed. Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("ERROR: Please enter numbers where required.")
        except mysql.connector.Error as e:
            print("Database ERROR:", e.msg)


main()
