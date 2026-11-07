from graphviz import Digraph

# Create a new Digraph with increased DPI
dot = Digraph(comment='Social Media Survey System', format='png', engine='dot', graph_attr={'size': '8.3,11.7', 'dpi': '300'})

# Define nodes with increased font size
dot.node('A', 'User Input\nName, Social Media Usage, DOB', width='1.5', height='1.5', fontsize='15')
dot.node('B', 'Submit Survey', width='1.5', height='0.8', fontsize='15')
dot.node('C', 'Show Survey Information', width='1.5', height='0.8', fontsize='15')
dot.node('D', 'Show User Information', width='1.5', height='0.8', fontsize='15')
dot.node('E', 'Show Particular Data', width='1.5', height='0.8', fontsize='15')
dot.node('F', 'Delete Data', width='1.5', height='0.8', fontsize='15')

# Define edges
dot.edges(['AB', 'AC', 'AD', 'AE', 'AF'])

# Save the Digraph to a file and render it as an image
dot.render('flowchart_a4', format='png', cleanup=True)
