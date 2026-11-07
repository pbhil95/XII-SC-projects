from tkinter import *
from tkinter import ttk
import mysql.connector

root = Tk()
root.configure(bg='#ffeae0')

# Connect to MySQL database
my_db = mysql.connector.connect(host='localhost', user='root', password='admin')
my_db_cursor = my_db.cursor()
my_db_cursor.execute('CREATE DATABASE IF NOT EXISTS survey')
my_db.commit()

my_db1 = mysql.connector.connect(host='localhost', user='root', password='admin', database='survey')
cur = my_db1.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS survey_info
            (
            id INT PRIMARY KEY,
            facebook VARCHAR(20),
            instagram VARCHAR(20),
            telegram VARCHAR(20),
            twitter VARCHAR(20),
            youtube VARCHAR(20),
            reddit VARCHAR(20),
            snapchat VARCHAR(20),
            whatsapp VARCHAR(20),
            quora VARCHAR(20),
            tiktok VARCHAR(20),
            most_time_spent VARCHAR(20),
            least_time_used VARCHAR(20)
            );''')

cur.execute('''CREATE TABLE IF NOT EXISTS user_info
           (
           roll INT PRIMARY KEY,
           name VARCHAR(255),
           date_of_birth DATE
           );''')



def submit():
    my_db1 = mysql.connector.connect(host='localhost', user='root', password='admin', database='survey')
    cur = my_db1.cursor()

    # Get the values of the checkboxes
    checkbox_values = ['Yes' if var.get() else 'No' for var in checkboxes]

    # Create a tuple with checkbox values and other data
    survey_values = (
        roll_entry.get(),checkbox_values[0], checkbox_values[1], checkbox_values[2], checkbox_values[3],
        checkbox_values[4], checkbox_values[5], checkbox_values[6], checkbox_values[7],
        checkbox_values[8], checkbox_values[9], clicked1.get(), clicked2.get()
    )

    b1 = 'INSERT INTO survey_info(id,facebook,instagram,telegram,twitter,youtube,reddit,snapchat,whatsapp,quora,tiktok,most_time_spent,least_time_used) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cur.execute(b1, survey_values)

    b2 = 'INSERT INTO user_info(roll, name, date_of_birth) VALUES(%s, %s, %s)'
    user_values = (roll_entry.get(), name_entry.get(), dob_entry.get())
    cur.execute(b2, user_values)

    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    
    for var in checkboxes:
        var.set('No')  # Reset checkboxes to 'No'
    clicked1.set('select')
    clicked2.set('select')
    dob_entry.delete(0, END)
    dob_entry.insert(0, 'YYYY-MM-DD')
    my_db1.commit()
    Label(root, text='Data Recorded', bg='#ffeae0').grid(columnspan=2)

def show_survey():
    A = Tk()
    A.configure(bg='#ffeae0')
    A.title("Survey Information")

    tree = ttk.Treeview(A)
    tree["columns"] = ("Id", "Facebook", "Instagram", "Telegram", "Twitter", "YouTube", "Reddit", "Snapchat",
                       "WhatsApp", "Quora", "TikTok", "Most Time Spent", "Least Time Used")

    # Define column headings
    tree.heading("Id", text="Id")
    tree.heading("Facebook", text="Facebook")
    tree.heading("Instagram", text="Instagram")
    tree.heading("Telegram", text="Telegram")
    tree.heading("Twitter", text="Twitter")
    tree.heading("YouTube", text="YouTube")
    tree.heading("Reddit", text="Reddit")
    tree.heading("Snapchat", text="Snapchat")
    tree.heading("WhatsApp", text="WhatsApp")
    tree.heading("Quora", text="Quora")
    tree.heading("TikTok", text="TikTok")
    tree.heading("Most Time Spent", text="Most Time Spent")
    tree.heading("Least Time Used", text="Least Time Used")

    # Set column widths statically
    tree.column("Id", width=50)
    tree.column("Facebook", width=60)
    tree.column("Instagram", width=70)
    tree.column("Telegram", width=60)
    tree.column("Twitter", width=60)
    tree.column("YouTube", width=60)
    tree.column("Reddit", width=60)
    tree.column("Snapchat", width=70)
    tree.column("WhatsApp", width=80)
    tree.column("Quora", width=60)
    tree.column("TikTok", width=60)
    tree.column("Most Time Spent", width=120)
    tree.column("Least Time Used", width=120)
    tree["show"] = "headings"  # Hide the default first column
    # Populate treeview with data
    cur.execute('SELECT * FROM survey_info')
    for row in cur:
        tree.insert("", "end", values=row)

    # Add treeview to the window
    tree.grid(row=1, column=0, padx=1, pady=1, columnspan=2, sticky="nsew")

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(A, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    A.mainloop()


def show_user_info():
    B = Tk()
    B.configure(bg='#ffeae0')
    B.title("User Information")

    tree = ttk.Treeview(B)
    tree["columns"] = ("Id","Name", "Date of Birth")

    # Define column headings with centered text
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor="center")

    # Set column widths
    for col in tree["columns"]:
        tree.column(col, width=100, anchor="center")  # Adjust the width as needed
        tree["show"] = "headings"  # Hide the default first column

    # Populate treeview with data
    cur.execute('SELECT * FROM user_info')
    for row in cur:
        tree.insert("", "end", values=row)

    # Add treeview to the window
    tree.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(B, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    B.mainloop()

def delete_data():
    if vall.get() == '':
        Label(C, text='Enter id', bg='#ffeae0').grid(columnspan=2)
    else:
        s = (int(vall.get()),)
        b2 = 'SELECT * FROM  user_info where roll=%s'
        cur.execute(b2, s)
        ch = ''
        for a in cur:
            ch = ch + str(a[0])
        if ch == '':
            Label(C, text=f'No data exists where id = {vall.get()}', bg='#ffeae0').grid(columnspan=2)
            vall.delete(0, END)
        elif ch != '':
            s = (int(vall.get()),)
            b = 'DELETE FROM survey_info where id=%s'
            cur.execute(b, s)
            b1 = 'DELETE FROM user_info where roll=%s'
            cur.execute(b1, s)
            Label(C, text='Data deleted', bg='#ffeae0').grid(columnspan=2)
            vall.delete(0, END)
            my_db1.commit()


def delete_data_window():
    global vall
    global C
    C = Tk()
    C.configure(bg='#ffeae0')
    Label(C, text='DELETE WINDOW', bg='#ffeae0').grid(row=0, column=0, columnspan=2)
    Label(C, text='Enter Id of data to be deleted', bg='#ffeae0').grid(row=1, column=0)
    vall = Entry(C)
    vall.grid(row=1, column=1)
    Button(C, text='DELETE DATA', command=delete_data).grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    C.mainloop()


def show_data():
    if valll.get() == '':
        Label(D, text='Enter id', bg='#ffeae0').grid(columnspan=2)
    else:
        s = (int(valll.get()),)
        b2 = 'SELECT * FROM user_info where roll=%s'
        cur.execute(b2, s)
        ch = ''
        for a in cur:
            ch = ch + str(a[0])
        if ch == '':
            Label(D, text=f'No data exists where id = {valll.get()}', bg='#ffeae0').grid(columnspan=2)
            valll.delete(0, END)
        elif ch != '':
            s = (int(valll.get()),)
            b = 'SELECT * FROM survey_info where id=%s'
            cur.execute(b, s)

            # Fetch all rows from the result set
            rows = cur.fetchall()

            E = Tk()
            E.configure(bg='#ffeae0')
            E.title("Data Information")

            tree = ttk.Treeview(E)
            tree["columns"] = ("Survey ID", "Facebook", "Instagram", "Telegram", "Twitter", "YouTube", "Reddit",
                               "Snapchat", "WhatsApp", "Quora", "TikTok", "Most Time Spent", "Least Time Used")

            # Configure column headings
            for col in tree["columns"]:
                tree.heading(col, text=col, anchor='center')
                tree.column(col, anchor='center', width=60)  # Adjust width as needed
                tree["show"] = "headings"  # Hide the default first column
            # Populate treeview with data using the fetched rows
            for row in rows:
                tree.insert("", "end", values=row)

            # Add a scrollbar to the treeview
            scrollbar = ttk.Scrollbar(E, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(expand=YES, fill=BOTH)
            valll.delete(0, END)
            my_db1.commit()
            E.mainloop()


def show_particular_data_window():
    global D
    global valll
    D = Tk()
    D.configure(bg='#ffeae0')
    Label(D, text='VIEW WINDOW', bg='#ffeae0').grid(row=0, column=0, columnspan=2)
    Label(D, text='Enter id of data to view', bg='#ffeae0').grid(row=1, column=0)
    valll = Entry(D)
    valll.grid(row=1, column=1)
    Button(D, text='VIEW', command=show_data).grid(row=2, columnspan=2)
    D.mainloop()


Label(root, text='Name', bg='#ffeae0').grid(row=0, column=0)
Label(root, text='Roll', bg='#ffeae0').grid(row=0, column=2)
Label(root, text='Select the social media sites you use:', bg='#ffeae0').grid(row=1, column=0)

checkboxes = []
options = [
    'facebook', 'instagram', 'telegram', 'twitter', 'youtube', 'reddit', 'snapchat', 'whatsapp', 'quora', 'tiktok'
]

# Create Checkbuttons in a grid layout
row_num = 2
col_num = 0
for option in options:
    var = BooleanVar()
    checkbox = Checkbutton(root, text=option, variable=var, onvalue=True, offvalue=False, justify='left', bg='#ffeae0')
    checkbox.deselect()
    checkbox.grid(row=row_num, column=col_num, sticky=W, padx=5, pady=5)
    checkboxes.append(var)

    col_num += 1
    if col_num == 5:  # Adjust the number of columns as needed
        col_num = 0
        row_num += 1
        

name_entry = Entry(root)
name_entry.grid(row=0, column=1)
name_entry.insert(0, '')

roll_entry = Entry(root)
roll_entry.grid(row=0, column=3)
name_entry.insert(0, '')

Label(root, text='which social media site you use most', bg='#ffeae0').grid(row=5, column=0)
Label(root, text='which social media site you use least', bg='#ffeae0').grid(row=6, column=0)

clicked1 = StringVar()
clicked1.set('select')
drop1 = OptionMenu(root, clicked1, *options)
drop1.grid(row=5, column=1)

clicked2 = StringVar()
clicked2.set('select')
drop2 = OptionMenu(root, clicked2, *options)
drop2.grid(row=6, column=1)

Label(root, text='Date of birth', bg='#ffeae0').grid(row=7, column=0)

dob_entry = Entry(root)
dob_entry.insert(0, 'YYYY-MM-DD')
dob_entry.grid(row=7, column=1)

Button(root, text='SUBMIT', command=submit).grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
my_db1.commit()

Button(root, text='SHOW SURVEY INFO', command=show_survey).grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

Button(root, text='SHOW USER INFO', command=show_user_info).grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

Button(root, text='SHOW PARTICULAR DATA', command=show_particular_data_window).grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

Button(root, text='DELETE DATA', command=delete_data_window).grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

root.mainloop()
