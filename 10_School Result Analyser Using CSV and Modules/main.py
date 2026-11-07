# main.py
# School Result Analyser - menu driven program
# Run this file. It uses our own modules fileops.py and analysis.py

import fileops
import analysis
from fileops import SUBJECTS


def get_marks(subject):
    while True:
        try:
            m = int(input("Enter marks in " + subject + " (0-100): "))
            if 0 <= m <= 100:
                return m
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a number.")


def display_all():
    students = fileops.read_marks()
    if len(students) == 0:
        print("No records found.")
        return
    print("%-5s %-16s %5s %5s %5s %5s %5s %6s %7s %5s %6s" %
          ("Roll", "Name", "Eng", "Phy", "Chem", "Math", "CS", "Total", "Per%", "Grade", "Result"))
    print("-" * 82)
    for s in students:
        t, p, g, r = analysis.student_summary(s)
        print("%-5s %-16s %5d %5d %5d %5d %5d %6d %7.2f %5s %6s" %
              (s[0], s[1], s[2], s[3], s[4], s[5], s[6], t, p, g, r))


def add_student():
    students = fileops.read_marks()
    roll = input("Enter Roll Number: ")
    for s in students:
        if s[0] == roll:
            print("Roll number already exists!")
            return
    name = input("Enter Student Name: ")
    row = [roll, name]
    for sub in SUBJECTS:
        row.append(get_marks(sub))
    fileops.add_marks(row)
    print("Marks of", name, "saved successfully.")


def search_student():
    roll = input("Enter Roll Number to search: ")
    for s in fileops.read_marks():
        if s[0] == roll:
            t, p, g, r = analysis.student_summary(s)
            print("Name:", s[1])
            for i in range(len(SUBJECTS)):
                print("  ", SUBJECTS[i], ":", s[i + 2])
            print("Total:", t, "| Percentage:", p, "| Grade:", g, "| Result:", r)
            return
    print("No student with roll number", roll)


def subject_toppers():
    students = fileops.read_marks()
    if len(students) == 0:
        print("No records found.")
        return
    print("Subject-wise Toppers")
    print("--------------------")
    for i in range(len(SUBJECTS)):
        name, marks = analysis.subject_topper(students, i + 2)
        print("%-10s : %-16s (%d)" % (SUBJECTS[i], name, marks))


def class_analysis():
    students = fileops.read_marks()
    if len(students) == 0:
        print("No records found.")
        return
    passed = 0
    grades = {}
    topper = ""
    top_per = -1
    for s in students:
        t, p, g, r = analysis.student_summary(s)
        if r == "PASS":
            passed = passed + 1
        grades[g] = grades.get(g, 0) + 1
        if p > top_per:
            top_per = p
            topper = s[1]
    print("Total Students :", len(students))
    print("Passed         :", passed)
    print("Failed         :", len(students) - passed)
    print("Pass Percentage:", round(passed * 100 / len(students), 2), "%")
    print("Class Average  :", analysis.class_average(students), "%")
    print("Class Topper   :", topper, "(", top_per, "% )")
    print("Grade Distribution:")
    for g in ["A1", "A2", "B1", "B2", "C1", "C2", "D", "E"]:
        if g in grades:
            print("  ", g, ":", "*" * grades[g], grades[g])


def generate_reports():
    students = fileops.read_marks()
    count = 0
    for s in students:
        t, p, g, r = analysis.student_summary(s)
        lines = []
        lines.append("REPORT CARD - CLASS XII\n")
        lines.append("Roll No : " + s[0] + "\n")
        lines.append("Name    : " + s[1] + "\n")
        lines.append("-" * 28 + "\n")
        for i in range(len(SUBJECTS)):
            lines.append("%-12s %5d\n" % (SUBJECTS[i], s[i + 2]))
        lines.append("-" * 28 + "\n")
        lines.append("Total      : " + str(t) + " / 500\n")
        lines.append("Percentage : " + str(p) + " %\n")
        lines.append("Grade      : " + g + "\n")
        lines.append("Result     : " + r + "\n")
        fileops.write_report(s[0], lines)
        count = count + 1
    print(count, "report cards created in the folder '" + fileops.REPORT_FOLDER + "'")


def view_report():
    roll = input("Enter Roll Number: ")
    content, position = fileops.read_report(roll)
    if content is None:
        print("Report not found. Generate report cards first (option 6).")
        return
    print("(File pointer after reading first line was at byte", position, ")")
    print(content)


def main():
    while True:
        print("\n====== SCHOOL RESULT ANALYSER ======")
        print("1. Display Result of All Students")
        print("2. Add Student Marks")
        print("3. Search Student")
        print("4. Subject-wise Toppers")
        print("5. Class Analysis")
        print("6. Generate Report Cards (text files)")
        print("7. View a Report Card")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_all()
        elif choice == "2":
            add_student()
        elif choice == "3":
            search_student()
        elif choice == "4":
            subject_toppers()
        elif choice == "5":
            class_analysis()
        elif choice == "6":
            generate_reports()
        elif choice == "7":
            view_report()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")


main()
