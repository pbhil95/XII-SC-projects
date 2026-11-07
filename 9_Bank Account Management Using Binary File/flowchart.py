from graphviz import Digraph

# Flowchart of Bank Account Management System
dot = Digraph('flowchart', format='png', graph_attr={'dpi': '150'})
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow', fontname='Arial')

dot.node('start', 'Start', shape='oval', fillcolor='lightgreen')
dot.node('menu', 'Display Menu\nEnter choice', shape='parallelogram', fillcolor='lightblue')
dot.node('create', 'Create Account\n(append record to accounts.dat)')
dot.node('read', 'Read all records from file\n(pickle.load until EOFError)')
dot.node('valid', 'Account exists and\nbalance enough?', shape='diamond', fillcolor='white')
dot.node('error', 'raise ValueError\nShow ERROR message')
dot.node('trans', 'Deposit / Withdraw /\nTransfer\nUpdate balance')
dot.node('write', 'Write all records to file\nPUSH transaction on stack')
dot.node('show', 'Balance Enquiry /\nDisplay All')
dot.node('undo', 'Undo: Is stack empty?', shape='diamond', fillcolor='white')
dot.node('empty', 'Nothing to undo')
dot.node('rev', 'POP transaction\nReverse it, save file')
dot.node('stop', 'Exit', shape='oval', fillcolor='lightcoral')

dot.edge('start', 'menu')
dot.edge('menu', 'create', label='1')
dot.edge('menu', 'read', label='2, 3, 4')
dot.edge('read', 'valid')
dot.edge('valid', 'error', label='No')
dot.edge('valid', 'trans', label='Yes')
dot.edge('trans', 'write')
dot.edge('menu', 'show', label='5, 6')
dot.edge('menu', 'undo', label='7')
dot.edge('undo', 'empty', label='Yes')
dot.edge('undo', 'rev', label='No')
dot.edge('menu', 'stop', label='8')
for n in ['create', 'error', 'write', 'show', 'empty', 'rev']:
    dot.edge(n, 'menu', style='dashed', color='gray')

dot.render('flowchart', cleanup=True)
print("Flowchart generated as 'flowchart.png'")
