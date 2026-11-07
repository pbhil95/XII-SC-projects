import time
import random

# File paths
users_file = 'users.txt'
questions_file = 'questions.txt'
results_file = 'results.txt'

# Helper functions
def load_users():
    users = {}
    try:
        with open(users_file, 'r') as f:
            for line in f:
                username, password, name, roll, cls, section, dob, role = line.strip().split(',')
                users[username] = {'password': password, 'name': name, 'roll': roll, 'class': cls, 'section': section, 'dob': dob, 'role': role}
    except FileNotFoundError:
        pass
    return users

def save_user(username, password, name, roll, cls, section, dob, role):
    with open(users_file, 'a') as f:
        f.write(f"{username},{password},{name},{roll},{cls},{section},{dob},{role}\n")

def generate_username(cls, section, roll):
    return f"{cls}{section}{str(roll).zfill(3)}"

def register():
    name = input("Enter your full name: ")
    roll = int(input("Enter roll number (1-50): "))
    while not (1 <= roll <= 50):
        print("Invalid roll number. Please enter a number between 1 and 50.")
        roll = int(input("Enter roll number (1-50): "))
    
    cls = input("Enter class (XI/XII): ").upper()
    while cls not in ["XI", "XII"]:
        print("Invalid class. Please enter XI or XII.")
        cls = input("Enter class (XI/XII): ").upper()
    
    section = input("Enter section (SC/HUM): ").upper()
    while section not in ["SC", "HUM"]:
        print("Invalid section. Please enter SC or HUM.")
        section = input("Enter section (SC/HUM): ").upper()
    
    dob = input("Enter date of birth (DD/MM/YYYY): ")
    password = input("Enter a password: ")
    
    username = generate_username(cls, section, roll)
    save_user(username, password, name, roll, cls, section, dob, 'user')
    print(f"Registration successful! Your username is {username}")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    users = load_users()
    if username in users and users[username]['password'] == password:
        return users[username]['role'], username
    else:
        print("Invalid credentials!")
        return None, None

# Admin Functions
def add_question():
    question = input("Enter question: ")
    options = [input(f"Option {chr(65+i)}: ") for i in range(4)]
    correct = input("Enter correct option (A/B/C/D): ").upper()
    category = input("Enter category: ")
    save_question(question, options, correct, category)
    print("Question added successfully!")

def save_question(question, options, correct, category):
    with open(questions_file, 'a') as f:
        f.write(f"{question}|{'|'.join(options)}|{correct}|{category}\n")

def load_questions():
    questions = []
    try:
        with open(questions_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    question_text = parts[0]
                    options = parts[1:5]
                    correct_answer = parts[5].upper()
                    category = parts[6]
                    questions.append({'question': question_text, 'options': options, 'correct': correct_answer, 'category': category})
    except FileNotFoundError:
        print("Questions file not found.")
    return questions

def view_questions():
    questions = load_questions()
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['question']}")
        for j, opt in enumerate(q['options']):
            print(f" {chr(65+j)}. {opt}")
        print(f"Correct: {q['correct']}, Category: {q['category']}\n")

def view_registered_users():
    users = load_users()
    print("\nRegistered Users:")
    for username, details in users.items():
        print(f"Username: {username}, Name: {details['name']}, Roll: {details['roll']}, Class: {details['class']}, Section: {details['section']}, DOB: {details['dob']}")

def leaderboard():
    results = load_results()
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    print("\nLeaderboard:")
    for result in sorted_results[:10]:  # Show top 10 performers
        print(f"Username: {result['username']}, Score: {result['score']}")

def load_results():
    results = []
    try:
        with open(results_file, 'r') as f:
            for line in f:
                username, score, correct, incorrect, time_taken = line.strip().split(',')
                results.append({'username': username, 'score': float(score), 'correct': int(correct), 'incorrect': int(incorrect), 'time_taken': int(time_taken)})
    except FileNotFoundError:
        pass
    return results

def save_result(username, score, correct, incorrect, time_taken):
    with open(results_file, 'a') as f:
        f.write(f"{username},{score},{correct},{incorrect},{time_taken}\n")

def view_all_results():
    results = load_results()
    print("\nAll Users' Quiz Participation:")
    for result in results:
        print(f"Username: {result['username']}, Score: {result['score']}, Correct: {result['correct']}, Incorrect: {result['incorrect']}, Time Taken: {result['time_taken']} seconds")

def search_user_result():
    username = input("Enter the username to search: ")
    results = load_results()
    user_found = False
    for result in results:
        if result['username'] == username:
            print(f"Username: {result['username']}, Score: {result['score']}, Correct: {result['correct']}, Incorrect: {result['incorrect']}, Time Taken: {result['time_taken']} seconds")
            user_found = True
    if not user_found:
        print("User result not found.")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Question")
        print("2. View Questions")
        print("3. View Registered Users")
        print("4. Leaderboard")
        print("5. View All Users' Results")
        print("6. Search User Result")
        print("7. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_question()
        elif choice == '2':
            view_questions()
        elif choice == '3':
            view_registered_users()
        elif choice == '4':
            leaderboard()
        elif choice == '5':
            view_all_results()
        elif choice == '6':
            search_user_result()
        elif choice == '7':
            break
        else:
            print("Invalid choice!")

# User Functions
def display_instructions():
    print("\nInstructions:")
    print("1. Each correct answer gives you 1 point.")
    print("2. Each incorrect answer will deduct 0.25 points.")
    print("3. You have limited time to complete the quiz.")
    print("4. Answer carefully!\n")

def play_quiz(username):
    questions = load_questions()
    if not questions:
        print("No questions available!")
        return
    
    random.shuffle(questions)  # Shuffle questions for random order
    total_questions = len(questions)
    correct_answers = 0
    incorrect_answers = 0
    start_time = time.time()
    time_limit = total_questions * 20  # 20 seconds per question

    display_instructions()

    for i, q in enumerate(questions):
        remaining_time = time_limit - (time.time() - start_time)
        if remaining_time <= 0:
            print("\nTime is up!")
            break
        print(f"\nQ{i+1}: {q['question']}")
        for j, opt in enumerate(q['options']):
            print(f" {chr(65+j)}. {opt}")
        print(f"Time remaining: {int(remaining_time)} seconds")
        answer = input("Your answer (A/B/C/D): ").upper()
        
        if answer == q['correct']:
            correct_answers += 1
        else:
            incorrect_answers += 1

    total_score = correct_answers * 1 - incorrect_answers * 0.25
    time_taken = int(time.time() - start_time)
    print(f"\nQuiz over! {username}'s score: {total_score}")
    print(f"Correct: {correct_answers}, Incorrect: {incorrect_answers}, Time taken: {time_taken} seconds")

    save_result(username, total_score, correct_answers, incorrect_answers, time_taken)

def user_menu(username):
    while True:
        print("\nUser Menu:")
        print("1. Play Quiz")
        print("2. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            play_quiz(username)
        elif choice == '2':
            break
        else:
            print("Invalid choice!")

# Main program
def main():
    print("Welcome to the Quiz Game!")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            role, username = login()
            if role == 'admin':
                admin_menu()
            elif role == 'user':
                user_menu(username)
        elif choice == '3':
            print("Thank you for using the Quiz Game!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
