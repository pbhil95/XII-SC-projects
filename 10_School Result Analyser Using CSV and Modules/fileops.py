# fileops.py
# User-defined module: all FILE related work (CSV file and text files)

import csv
import os

MARKS_FILE = "marks.csv"
REPORT_FOLDER = "reports"
SUBJECTS = ["English", "Physics", "Chemistry", "Maths", "CS"]


def read_marks():
    # Returns a list of students. Each student is a list:
    # [roll, name, m1, m2, m3, m4, m5]  (marks are converted to int)
    students = []
    if not os.path.exists(MARKS_FILE):
        return students
    f = open(MARKS_FILE, "r", newline="")
    reader = csv.reader(f)
    next(reader)                      # skip the heading row
    for row in reader:
        student = [row[0], row[1]]
        for m in row[2:]:
            student.append(int(m))
        students.append(student)
    f.close()
    return students


def add_marks(row):
    # Append one student row to the CSV file
    new_file = not os.path.exists(MARKS_FILE)
    f = open(MARKS_FILE, "a", newline="")
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["RollNo", "Name"] + SUBJECTS)
    writer.writerow(row)
    f.close()


def write_report(roll, lines):
    # Write a report card (list of lines) into a text file
    if not os.path.exists(REPORT_FOLDER):
        os.mkdir(REPORT_FOLDER)
    file_name = REPORT_FOLDER + "/report_" + roll + ".txt"
    f = open(file_name, "w")
    f.writelines(lines)
    f.close()
    return file_name


def read_report(roll):
    # Read a report card text file and show tell() / seek() use
    file_name = REPORT_FOLDER + "/report_" + roll + ".txt"
    if not os.path.exists(file_name):
        return None, 0
    f = open(file_name, "r")
    first_line = f.readline()          # read only the first line
    position = f.tell()                # where the file pointer is now
    f.seek(0)                          # go back to the beginning
    content = f.read()                 # read the whole file
    f.close()
    return content, position
