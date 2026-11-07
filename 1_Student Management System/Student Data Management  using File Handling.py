import csv
import os

DATA_FILE = "student_data.csv"

def display_menu():
    print("1. Add Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. Search Student")
    print("5. Display Students")
    print("6. Exit")

def add_student(admno, name, course, fees, dob):
    with open(DATA_FILE, mode='a', newline='') as file:
        csv.writer(file).writerow([admno, name, course, fees, dob])
    print("Student added successfully!")

def update_student(admno, name, course, fees, dob):
    data = load_from_file()
    found = False

    for i, row in enumerate(data):
        if row[0] == str(admno):
            data[i] = [str(admno), name, course, str(fees), dob]
            found = True
            break

    if found:
        write_to_file(data)
        print("Student updated successfully!")
    else:
        print("No student found with Admission Number:", admno)

def delete_student(admno):
    data = load_from_file()
    found = False

    for i, row in enumerate(data):
        if row[0] == str(admno):
            del data[i]
            found = True
            break

    if found:
        write_to_file(data)
        print("Student deleted successfully!")
    else:
        print("No student found with Admission Number:", admno)

def search_student(admno):
    data = load_from_file()
    student = next((row for row in data if row[0] == str(admno)), None)
    if student:
        print_student_details(student)
    else:
        print("No student found with Admission Number:", admno)

def display_students():
    data = load_from_file()
    if data:
        print("List of Students:")
        print("--------------------------")
        for row in data:
            print_student_details(row)
    else:
        print("No students found.")

def print_student_details(student):
    admno, name, course, fees, dob = student
    print(f"Admission Number: {admno}")
    print(f"Name: {name}")
    print(f"Course: {course}")
    print(f"Fees: {fees}")
    print(f"Date of Birth: {dob}")
    print("--------------------------")

def load_from_file():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
    return data

def write_to_file(data):
    with open(DATA_FILE, "w", newline='') as file:
        csv.writer(file).writerows(data)

def main():
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            admno, name, course, fees, dob = get_student_input()
            add_student(admno, name, course, fees, dob)

        elif choice == 2:
            admno, name, course, fees, dob = get_student_input()
            update_student(admno, name, course, fees, dob)

        elif choice == 3:
            admno = int(input("Enter Admission Number of student to delete: "))
            delete_student(admno)

        elif choice == 4:
            admno = input("Enter Admission Number of student to search: ")
            search_student(admno)

        elif choice == 5:
            display_students()

        elif choice == 6:
            break

        else:
            print("Invalid choice! Please try again.")

def get_student_input():
    admno = int(input("Enter Admission Number: "))
    name = input("Enter Name: ")
    course = input("Enter Course: ")
    fees = float(input("Enter Fees: "))
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    return admno, name, course, fees, dob

if __name__ == "__main__":
    main()
