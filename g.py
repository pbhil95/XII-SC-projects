from graphviz import Digraph

# Create a new Digraph
flowchart = Digraph('flowchart', format='png', engine='dot',graph_attr={'size': '8.3,11.7', 'dpi': '300'})
# Define nodes
flowchart.node('start', 'Start')
flowchart.node('load_words', 'Load words from file')
flowchart.node('guess', 'Make a guess')
flowchart.node('play_again', 'Ask to play again')
flowchart.node('end', 'End')

# Define edges
flowchart.edge('start', 'load_words')
flowchart.edge('load_words', 'guess', label='Select a random word')
flowchart.edge('guess', 'guess', label='Continue guessing')
flowchart.edge('guess', 'play_again', label='Exhausted all tries')
flowchart.edge('play_again', 'start', label='Yes')
flowchart.edge('play_again', 'end', label='No')

# Save the flowchart as a PNG file
flowchart.render('flowchart', format='png', cleanup=True)

print("Flowchart generated as 'flowchart.png'")
