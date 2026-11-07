import pickle
import os
import uuid  # For generating unique student IDs

# Files to store library and student data
library_data_file = 'library_data.pkl'
students_data_file = 'students_data.pkl'

# Librarian credentials (can be hardcoded for simplicity)
LIBRARIAN_USERNAME = "Pankaj"
LIBRARIAN_PASSWORD = "qwer"

# Function to load data from a pickle file
def load_data(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


# Function to save data to a pickle file
def save_data(data, file):
    with open(file, 'wb') as f:
        pickle.dump(data, f)


# Function to register students with extended details and auto-generated ID
def register_student():
    students = load_data(students_data_file)
    
    name = input("Enter Student Name: ")
    roll = input("Enter Roll Number: ")
    student_class = input("Enter Class: ")
    section = input("Enter Section: ")
    gender = input("Enter Gender (M/F): ")
    dob = input("Enter Date of Birth (DD-MM-YYYY): ")
    
    # Generate a unique student ID
    student_id = str(uuid.uuid4())[:8]  # Using first 8 characters of UUID as student ID
    
    # Register the student with details
    students[student_id] = {
        'name': name,
        'roll': roll,
        'class': student_class,
        'section': section,
        'gender': gender,
        'dob': dob,
        'issued_books': [],
        'books_returned': 0
    }
    
    save_data(students, students_data_file)
    print(f"Student '{name}' registered successfully with Student ID: {student_id}")


# Function to authenticate librarian
def authenticate_librarian():
    username = input("Enter librarian username: ")
    password = input("Enter librarian password: ")

    if username == LIBRARIAN_USERNAME and password == LIBRARIAN_PASSWORD:
        print("Librarian authenticated successfully!")
        return True
    else:
        print("Authentication failed! Invalid username or password.")
        return False


# Function to add a book to the library
def add_book(book_id, title, author):
    library = load_data(library_data_file)
    if book_id in library:
        print(f"Book with ID {book_id} already exists!")
    else:
        library[book_id] = {'title': title, 'author': author, 'is_issued': False, 'issued_to': None}
        save_data(library, library_data_file)
        print(f"Book '{title}' added successfully!")


# Function to remove a book from the library
def remove_book(book_id):
    library = load_data(library_data_file)
    if book_id in library:
        del library[book_id]
        save_data(library, library_data_file)
        print(f"Book ID {book_id} removed successfully!")
    else:
        print(f"Book with ID {book_id} not found!")


# Function to issue a book to a registered student, checking conditions
def issue_book(student_id):
    library = load_data(library_data_file)
    students = load_data(students_data_file)

    if student_id not in students:
        print(f"Student with ID {student_id} is not registered!")
        return

    student = students[student_id]
    
    # Check if the student has already issued the maximum of 10 books
    if len(student['issued_books']) >= 10:
        print(f"Student {student['name']} has already issued the maximum of 10 books!")
        return

    while True:
        book_id = input("Enter Book ID to issue: ")
        
        if book_id not in library:
            print(f"Book with ID {book_id} not found!")
            return

        if library[book_id]['is_issued']:
            print(f"Book ID {book_id} is already issued to {library[book_id]['issued_to']}!")
            return

        if book_id in student['issued_books']:
            print(f"Student {student['name']} has already issued this book.")
            return

        # Issue the book
        library[book_id]['is_issued'] = True
        library[book_id]['issued_to'] = student['name']
        student['issued_books'].append(book_id)

        save_data(library, library_data_file)
        save_data(students, students_data_file)

        print(f"Book ID {book_id} issued successfully to {student['name']}!")
        
        # Ask if the student wants to issue more books
        issue_more = input("Do you want to issue another book? (Y/N): ").strip().upper()
        if issue_more != 'Y':
            break


# Function to return a book by a student
def return_book(book_id, student_id):
    library = load_data(library_data_file)
    students = load_data(students_data_file)

    if book_id not in library:
        print(f"Book with ID {book_id} not found!")
        return

    if not library[book_id]['is_issued']:
        print(f"Book ID {book_id} is not issued!")
        return

    if student_id not in students:
        print(f"Student with ID {student_id} not registered!")
        return

    student = students[student_id]

    if book_id not in student['issued_books']:
        print(f"Student {student['name']} did not issue this book.")
        return

    # Return the book
    library[book_id]['is_issued'] = False
    library[book_id]['issued_to'] = None
    student['issued_books'].remove(book_id)
    student['books_returned'] += 1

    save_data(library, library_data_file)
    save_data(students, students_data_file)

    print(f"Book ID {book_id} returned successfully by {student['name']}!")


# Function to display all books
def display_books():
    library = load_data(library_data_file)
    if library:
        for book_id, book_info in library.items():
            status = 'Issued' if book_info['is_issued'] else 'Available'
            issued_to = book_info['issued_to'] if book_info['is_issued'] else 'N/A'
            print(f"Book ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Status: {status}, Issued To: {issued_to}")
    else:
        print("No books in the library.")


# Function to display all registered students
def display_students():
    students = load_data(students_data_file)
    if students:
        print("Registered Students:")
        for student_id, student_info in students.items():
            print(f"Student ID: {student_id}, Name: {student_info['name']}, Class: {student_info['class']}, Section: {student_info['section']}, Issued Books: {len(student_info['issued_books'])}, Books Returned: {student_info['books_returned']}")
    else:
        print("No students registered.")


# Main Program
if __name__ == "__main__":
    if authenticate_librarian():  # Only proceed if librarian is authenticated
        while True:
            print("\nLibrary Management System")
            print("1. Register Student")
            print("2. Add Book")
            print("3. Remove Book")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. Display Books")
            print("7. Display Students")
            print("8. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                register_student()

            elif choice == '2':
                book_id = input("Enter Book ID: ")
                title = input("Enter Book Title: ")
                author = input("Enter Book Author: ")
                add_book(book_id, title, author)

            elif choice == '3':
                book_id = input("Enter Book ID to remove: ")
                remove_book(book_id)

            elif choice == '4':
                student_id = input("Enter Student ID: ")
                issue_book(student_id)

            elif choice == '5':
                book_id = input("Enter Book ID to return: ")
                student_id = input("Enter Student ID: ")
                return_book(book_id, student_id)

            elif choice == '6':
                display_books()

            elif choice == '7':
                display_students()

            elif choice == '8':
                print("Exiting...")
                break

            else:
                print("Invalid choice! Please try again.")
