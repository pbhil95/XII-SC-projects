from graphviz import Digraph

# Create a new directed graph
flowchart = Digraph()

# Start node
flowchart.node('Start', 'Start')

# Librarian Authentication
flowchart.node('Auth', 'Librarian Authentication')
flowchart.edge('Start', 'Auth')

# Student Registration
flowchart.node('Reg', 'Student Registration')
flowchart.edge('Auth', 'Reg')

# Book Management
flowchart.node('BM', 'Book Management (Add/Remove Books)')
flowchart.edge('Reg', 'BM')

# Check branches for issue and return
flowchart.node('Issue', 'Issue Books')
flowchart.edge('BM', 'Issue')

flowchart.node('Return', 'Return Books')
flowchart.edge('BM', 'Return')

# Checks for issuing books
flowchart.node('Avail', 'Check if Book is Available')
flowchart.edge('Issue', 'Avail')

flowchart.node('NotIssued', 'Check if Book is Not Already Issued')
flowchart.edge('Avail', 'NotIssued')

# Checks for returning books
flowchart.node('Issued', 'Check if Book is Issued to Student')
flowchart.edge('Return', 'Issued')

# Decision points for further actions
flowchart.node('IssueMore', 'Issue More Books?')
flowchart.edge('NotIssued', 'IssueMore')

flowchart.node('ReturnMore', 'Return More Books?')
flowchart.edge('Issued', 'ReturnMore')

# Ending or Looping back
flowchart.node('Exit', 'Exit')
flowchart.edge('IssueMore', 'BM', label='Yes')
flowchart.edge('ReturnMore', 'BM', label='Yes')
flowchart.edge('IssueMore', 'Exit', label='No')
flowchart.edge('ReturnMore', 'Exit', label='No')

# Render the flowchart to a file
flowchart.render('library_management_flowchart', format='png', cleanup=False)
