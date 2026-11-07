# analysis.py
# User-defined module: all CALCULATIONS on marks


def total(marks):
    t = 0
    for m in marks:
        t = t + m
    return t


def percentage(total_marks, subjects=5, max_marks=100):
    # Default arguments: 5 subjects of 100 marks each
    return round(total_marks * 100 / (subjects * max_marks), 2)


def grade(per):
    # CBSE style grades
    if per >= 91:
        return "A1"
    elif per >= 81:
        return "A2"
    elif per >= 71:
        return "B1"
    elif per >= 61:
        return "B2"
    elif per >= 51:
        return "C1"
    elif per >= 41:
        return "C2"
    elif per >= 33:
        return "D"
    else:
        return "E"


def result(marks, pass_marks=33):
    # A student passes only if every subject has at least 33 marks
    for m in marks:
        if m < pass_marks:
            return "FAIL"
    return "PASS"


def student_summary(student):
    # Returns MORE THAN ONE value (a tuple)
    marks = student[2:]
    t = total(marks)
    p = percentage(t)
    return t, p, grade(p), result(marks)


def subject_topper(students, index):
    # index = position of the subject in the student list (2 to 6)
    best = students[0]
    for s in students:
        if s[index] > best[index]:
            best = s
    return best[1], best[index]


def class_average(students):
    if len(students) == 0:
        return 0
    sum_per = 0
    for s in students:
        t, p, g, r = student_summary(s)
        sum_per = sum_per + p
    return round(sum_per / len(students), 2)
