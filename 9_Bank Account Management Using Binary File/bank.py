# Bank Account Management System
# Uses: Binary file (pickle), Exception handling, Stack (for UNDO)

import pickle

FILE_NAME = "accounts.dat"
MIN_BALANCE = 500

# Stack to remember transactions of this session (for UNDO)
# Each item: [type, account_no, amount, to_account]
transactions = []


# ---------------- File handling ----------------

def read_all_accounts():
    # Read every record (dictionary) from the binary file
    accounts = []
    f = None
    try:
        f = open(FILE_NAME, "rb")
        while True:
            acc = pickle.load(f)
            accounts.append(acc)
    except FileNotFoundError:
        pass                    # first run: file does not exist yet
    except EOFError:
        pass                    # end of file reached
    finally:
        if f is not None:
            f.close()
    return accounts


def write_all_accounts(accounts):
    f = open(FILE_NAME, "wb")
    for acc in accounts:
        pickle.dump(acc, f)
    f.close()


def find_account(accounts, acc_no):
    for acc in accounts:
        if acc["acc_no"] == acc_no:
            return acc
    return None


# ---------------- Input helpers ----------------

def get_number(message):
    # Keep asking until a valid whole number is entered
    while True:
        try:
            num = int(input(message))
            if num <= 0:
                print("Please enter a number greater than 0.")
            else:
                return num
        except ValueError:
            print("Invalid input! Please enter digits only.")


def get_account(accounts, message):
    acc_no = get_number(message)
    acc = find_account(accounts, acc_no)
    if acc is None:
        raise ValueError("Account " + str(acc_no) + " does not exist.")
    return acc


# ---------------- Menu options ----------------

def create_account():
    accounts = read_all_accounts()
    if len(accounts) == 0:
        acc_no = 1001
    else:
        acc_no = accounts[-1]["acc_no"] + 1

    name = input("Enter Account Holder Name: ")
    acc_type = input("Enter Account Type (S-Saving / C-Current): ").upper()
    if acc_type == "C":
        acc_type = "Current"
    else:
        acc_type = "Saving"
    amount = get_number("Enter Opening Amount (minimum Rs. 500): ")
    if amount < MIN_BALANCE:
        raise ValueError("Opening amount must be at least Rs. 500.")

    acc = {"acc_no": acc_no, "name": name, "type": acc_type, "balance": amount}
    f = open(FILE_NAME, "ab")    # append a new record
    pickle.dump(acc, f)
    f.close()
    print("Account created successfully! Your Account Number is", acc_no)


def deposit():
    accounts = read_all_accounts()
    acc = get_account(accounts, "Enter Account Number: ")
    amount = get_number("Enter amount to deposit: ")
    acc["balance"] = acc["balance"] + amount
    write_all_accounts(accounts)
    transactions.append(["DEPOSIT", acc["acc_no"], amount, 0])
    print("Rs.", amount, "deposited. New Balance: Rs.", acc["balance"])


def withdraw():
    accounts = read_all_accounts()
    acc = get_account(accounts, "Enter Account Number: ")
    amount = get_number("Enter amount to withdraw: ")
    if acc["balance"] - amount < MIN_BALANCE:
        raise ValueError("Insufficient balance! Minimum balance Rs. 500 must remain.")
    acc["balance"] = acc["balance"] - amount
    write_all_accounts(accounts)
    transactions.append(["WITHDRAW", acc["acc_no"], amount, 0])
    print("Rs.", amount, "withdrawn. New Balance: Rs.", acc["balance"])


def transfer():
    accounts = read_all_accounts()
    sender = get_account(accounts, "Enter YOUR Account Number: ")
    receiver = get_account(accounts, "Enter RECEIVER Account Number: ")
    if sender["acc_no"] == receiver["acc_no"]:
        raise ValueError("Sender and receiver cannot be the same.")
    amount = get_number("Enter amount to transfer: ")
    if sender["balance"] - amount < MIN_BALANCE:
        raise ValueError("Insufficient balance! Minimum balance Rs. 500 must remain.")
    sender["balance"] = sender["balance"] - amount
    receiver["balance"] = receiver["balance"] + amount
    write_all_accounts(accounts)
    transactions.append(["TRANSFER", sender["acc_no"], amount, receiver["acc_no"]])
    print("Rs.", amount, "transferred from", sender["acc_no"], "to", receiver["acc_no"])


def balance_enquiry():
    accounts = read_all_accounts()
    acc = get_account(accounts, "Enter Account Number: ")
    print("Account No :", acc["acc_no"])
    print("Name       :", acc["name"])
    print("Type       :", acc["type"])
    print("Balance    : Rs.", acc["balance"])


def display_all():
    accounts = read_all_accounts()
    if len(accounts) == 0:
        print("No accounts found.")
        return
    print("%-8s %-20s %-8s %10s" % ("Acc No", "Name", "Type", "Balance"))
    print("-" * 50)
    for acc in accounts:
        print("%-8d %-20s %-8s %10d" % (acc["acc_no"], acc["name"], acc["type"], acc["balance"]))


def undo_last():
    if len(transactions) == 0:
        print("Nothing to undo! (Stack is empty)")
        return
    last = transactions.pop()        # POP from stack
    kind, acc_no, amount, to_acc = last
    accounts = read_all_accounts()
    acc = find_account(accounts, acc_no)

    if kind == "DEPOSIT":
        acc["balance"] = acc["balance"] - amount
    elif kind == "WITHDRAW":
        acc["balance"] = acc["balance"] + amount
    elif kind == "TRANSFER":
        receiver = find_account(accounts, to_acc)
        acc["balance"] = acc["balance"] + amount
        receiver["balance"] = receiver["balance"] - amount
    write_all_accounts(accounts)
    print("Undo successful:", kind, "of Rs.", amount, "on account", acc_no, "reversed.")


def main():
    while True:
        print("\n======= BANK MANAGEMENT SYSTEM =======")
        print("1. Create New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Balance Enquiry")
        print("6. Display All Accounts")
        print("7. Undo Last Transaction")
        print("8. Exit")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                create_account()
            elif choice == "2":
                deposit()
            elif choice == "3":
                withdraw()
            elif choice == "4":
                transfer()
            elif choice == "5":
                balance_enquiry()
            elif choice == "6":
                display_all()
            elif choice == "7":
                undo_last()
            elif choice == "8":
                print("Thank you for banking with us!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError as error:
            print("ERROR:", error)


main()
