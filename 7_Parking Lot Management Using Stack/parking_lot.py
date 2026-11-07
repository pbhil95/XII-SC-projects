# Parking Lot Management System using Stack
# The parking lane is closed at one end, so the car that came in LAST
# must go out FIRST (LIFO). This is exactly how a STACK works.

import pickle
import os
import time

FILE_NAME = "parking_data.dat"   # binary file to save the lane
MAX_SIZE = 5                     # maximum cars the lane can hold
RATE_PER_HOUR = 20               # parking charge in Rupees


# ---------------- File handling ----------------

def load_lane():
    # Read the stack (list) from the binary file
    if os.path.exists(FILE_NAME):
        f = open(FILE_NAME, "rb")
        lane = pickle.load(f)
        f.close()
        return lane
    return []


def save_lane(lane):
    # Write the stack (list) to the binary file
    f = open(FILE_NAME, "wb")
    pickle.dump(lane, f)
    f.close()


# ---------------- Stack operations ----------------

def is_empty(lane):
    return len(lane) == 0


def is_full(lane):
    return len(lane) == MAX_SIZE


def push(lane, car):
    lane.append(car)


def pop(lane):
    return lane.pop()


def peek(lane):
    return lane[-1]


# ---------------- Helper functions ----------------

def calculate_fee(entry_time):
    # Every started hour is charged
    seconds = time.time() - entry_time
    hours = int(seconds // 3600) + 1
    return hours * RATE_PER_HOUR


def show_car(car):
    print("Car No:", car[0], "| Owner:", car[1], "| Entry Time:", car[2])


# ---------------- Menu options ----------------

def park_car(lane):
    if is_full(lane):
        print("OVERFLOW! Parking lane is full. No space for a new car.")
        return
    car_no = input("Enter Car Number: ").upper()
    for car in lane:
        if car[0] == car_no:
            print("This car is already parked.")
            return
    owner = input("Enter Owner Name: ")
    entry_text = time.strftime("%d-%m-%Y %H:%M")
    car = [car_no, owner, entry_text, time.time()]
    push(lane, car)
    save_lane(lane)
    print("Car", car_no, "parked successfully at position", len(lane))


def remove_last_car(lane):
    if is_empty(lane):
        print("UNDERFLOW! Parking lane is empty.")
        return
    car = pop(lane)
    save_lane(lane)
    print("Car", car[0], "has left the parking.")
    print("Parking Fee: Rs.", calculate_fee(car[3]))


def remove_any_car(lane):
    if is_empty(lane):
        print("UNDERFLOW! Parking lane is empty.")
        return
    car_no = input("Enter Car Number to remove: ").upper()

    found = False
    for car in lane:
        if car[0] == car_no:
            found = True
    if not found:
        print("Car", car_no, "is not in the parking lane.")
        return

    temp = []    # temporary stack (waiting area outside the lane)
    # Move cars in front of the required car to the temporary stack
    while peek(lane)[0] != car_no:
        moved = pop(lane)
        push(temp, moved)
        print("Moved car", moved[0], "out to waiting area")

    car = pop(lane)
    print("Car", car[0], "has left the parking.")
    print("Parking Fee: Rs.", calculate_fee(car[3]))

    # Bring the moved cars back into the lane
    while not is_empty(temp):
        moved = pop(temp)
        push(lane, moved)
        print("Car", moved[0], "parked back in the lane")
    save_lane(lane)


def show_gate_car(lane):
    if is_empty(lane):
        print("Parking lane is empty.")
    else:
        print("Car nearest to the gate (TOP of stack):")
        show_car(peek(lane))


def display_lane(lane):
    if is_empty(lane):
        print("Parking lane is empty.")
        return
    print("------------- GATE -------------")
    for i in range(len(lane) - 1, -1, -1):
        print("Position", i + 1, end=": ")
        show_car(lane[i])
    print("------------ WALL --------------")
    print("Cars parked:", len(lane), "| Free spaces:", MAX_SIZE - len(lane))


def search_car(lane):
    car_no = input("Enter Car Number to search: ").upper()
    for i in range(len(lane)):
        if lane[i][0] == car_no:
            show_car(lane[i])
            cars_in_front = len(lane) - 1 - i
            print("Cars to be moved to take it out:", cars_in_front)
            return
    print("Car", car_no, "is not in the parking lane.")


def main():
    lane = load_lane()
    while True:
        print("\n===== PARKING LOT MANAGEMENT =====")
        print("1. Park a Car (PUSH)")
        print("2. Remove Last Parked Car (POP)")
        print("3. Remove Any Car")
        print("4. Show Car Near Gate (PEEK)")
        print("5. Display Parking Lane")
        print("6. Search a Car")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            park_car(lane)
        elif choice == "2":
            remove_last_car(lane)
        elif choice == "3":
            remove_any_car(lane)
        elif choice == "4":
            show_gate_car(lane)
        elif choice == "5":
            display_lane(lane)
        elif choice == "6":
            search_car(lane)
        elif choice == "7":
            print("Thank you! Data saved in", FILE_NAME)
            break
        else:
            print("Invalid choice! Please try again.")


main()
