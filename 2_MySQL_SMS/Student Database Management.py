import mysql.connector

def display_menu():
    print("1. Add Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. Search Student")
    print("5. Display Students")
    print("6. Exit")
    
def create_database_school():
    try:
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",
            )
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS school')
        cursor.execute('USE school')
        connection.commit()
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to connect to database:", error)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="school"
        )
        print("Connected to database successfully!")
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database:", error)

def create_table(cursor):
    table_query = """
        CREATE TABLE IF NOT EXISTS student (
            admno INT PRIMARY KEY,
            name VARCHAR(100),
            course VARCHAR(50),
            fees FLOAT,
            dob DATE
        )
    """
    cursor.execute(table_query)
    print("Table created successfully!")

def add_student(connection, cursor):
    admno = int(input("Enter Admission Number: "))
    name = input("Enter Name: ")
    course = input("Enter Course: ")
    fees = float(input("Enter Fees: "))
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")

    insert_query = f"""INSERT INTO
                    student(admno, name, course,fees, dob)
                    VALUES ({admno}, '{name}', '{course}',
                    {fees}, '{dob}')"""
    cursor.execute(insert_query)
    connection.commit()

    print("Student added successfully!")

def update_student(connection, cursor):
    admno = int(input("Enter Admission Number of student to update: "))

    name = input("Enter Name: ")
    course = input("Enter Course: ")
    fees = float(input("Enter Fees: "))
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    update_query = f"""
        UPDATE student
        SET name = '{name}', course = '{course}',
        fees = {fees}, dob = '{dob}'
        WHERE admno = {admno}"""
    cursor.execute(update_query)
    connection.commit()
    if cursor.rowcount > 0:
        print("Student updated successfully!")
    else:
        print("No student found with Admission Number:", admno)

def delete_student(connection, cursor):
    admno = int(input("Enter Admission Number of student to delete: "))

    delete_query = f"""
        DELETE FROM student
        WHERE admno = {admno}"""
    cursor.execute(delete_query)
    connection.commit()
    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("No student found with Admission Number:", admno)

def search_student(cursor):
    admno = int(input("Enter Admission Number of student to search: "))

    search_query =f"""
        SELECT * FROM student
        WHERE admno = {admno}"""
    cursor.execute(search_query)
    result = cursor.fetchone()

    if result:
        print("Admission Number:", result[0])
        print("Name:", result[1])
        print("Course:", result[2])
        print("Fees:", result[3])
        print("Date of Birth:", result[4])
    else:
        print("No student found with Admission Number:", admno)

def display_students(cursor):
    select_query = """
        SELECT * FROM student
    """

    cursor.execute(select_query)
    result = cursor.fetchall()

    if result:
        for row in result:
            print("Admission Number:", row[0])
            print("Name:", row[1])
            print("Course:", row[2])
            print("Fees:", row[3])
            print("Date of Birth:", row[4])
            print("--------------")
    else:
        print("No students found.")

def main():
    create_database_school()
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()
    create_table(cursor)

    while True:
        display_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_student(connection, cursor)
        elif choice == 2:
            update_student(connection, cursor)
        elif choice == 3:
            delete_student(connection, cursor)
        elif choice == 4:
            search_student(cursor)
        elif choice == 5:
            display_students(cursor)
        elif choice == 6:
            break
        else:
            print("Invalid choice! Please try again.")

    connection.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
