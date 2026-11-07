from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Quiz Game Flow')

# Main program flow
dot.node('Start', 'Start Program')
dot.node('Register', 'Register')
dot.node('Login', 'Login')
dot.node('Exit', 'Exit Program')
dot.node('Main Menu', 'Main Menu')

# Registration flow
dot.node('Enter Name', 'Enter Full Name')
dot.node('Enter Roll', 'Enter Roll Number (1-50)')
dot.node('Enter Class', 'Enter Class (XI/XII)')
dot.node('Enter Section', 'Enter Section (SC/HUM)')
dot.node('Enter DOB', 'Enter Date of Birth')
dot.node('Enter Password', 'Enter Password')
dot.node('Save User', 'Save User')
dot.node('Show Username', 'Show Username')
dot.node('Registration Done', 'Registration Successful')

# Login flow
dot.node('Enter Username', 'Enter Username')
dot.node('Enter Password', 'Enter Password')
dot.node('Validate User', 'Validate User Credentials')
dot.node('Admin Menu', 'Admin Menu')
dot.node('User Menu', 'User Menu')
dot.node('Invalid Login', 'Invalid Credentials')

# User menu flow
dot.node('Play Quiz', 'Play Quiz')
dot.node('Display Instructions', 'Display Quiz Instructions')
dot.node('Start Quiz', 'Start Quiz')
dot.node('End Quiz', 'End Quiz')
dot.node('Save Result', 'Save Result')
dot.node('Logout', 'Logout')

# Admin menu flow
dot.node('Add Question', 'Add Question')
dot.node('View Questions', 'View Questions')
dot.node('View Users', 'View Registered Users')
dot.node('Leaderboard', 'Leaderboard')
dot.node('View Results', 'View All Results')
dot.node('Search Result', 'Search User Result')
dot.node('Admin Logout', 'Logout')

# Main program connections
dot.edges([('Start', 'Main Menu'),
           ('Main Menu', 'Register'),
           ('Main Menu', 'Login'),
           ('Main Menu', 'Exit')])

# Registration connections
dot.edges([('Register', 'Enter Name'),
           ('Enter Name', 'Enter Roll'),
           ('Enter Roll', 'Enter Class'),
           ('Enter Class', 'Enter Section'),
           ('Enter Section', 'Enter DOB'),
           ('Enter DOB', 'Enter Password'),
           ('Enter Password', 'Save User'),
           ('Save User', 'Show Username'),
           ('Show Username', 'Registration Done'),
           ('Registration Done', 'Main Menu')])

# Login connections
dot.edges([('Login', 'Enter Username'),
           ('Enter Username', 'Enter Password'),
           ('Enter Password', 'Validate User')])

# Admin/User menu connections
dot.edge('Validate User', 'Admin Menu', label='Admin')
dot.edge('Validate User', 'User Menu', label='User')
dot.edge('Validate User', 'Invalid Login', label='Invalid')
dot.edge('Invalid Login', 'Main Menu')

# User menu connections
dot.edges([('User Menu', 'Play Quiz'),
           ('User Menu', 'Logout')])
dot.edges([('Play Quiz', 'Display Instructions'),
           ('Display Instructions', 'Start Quiz'),
           ('Start Quiz', 'End Quiz'),
           ('End Quiz', 'Save Result'),
           ('Save Result', 'User Menu')])

# Admin menu connections
dot.edges([('Admin Menu', 'Add Question'),
           ('Admin Menu', 'View Questions'),
           ('Admin Menu', 'View Users'),
           ('Admin Menu', 'Leaderboard'),
           ('Admin Menu', 'View Results'),
           ('Admin Menu', 'Search Result'),
           ('Admin Menu', 'Admin Logout')])

# Logout connections
dot.edge('Admin Logout', 'Main Menu')
dot.edge('Logout', 'Main Menu')

# Render the flowchart to a file and display it
dot.render('/mnt/data/quiz_game_flowchart', format='png')

'/mnt/data/quiz_game_flowchart.png'
