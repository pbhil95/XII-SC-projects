from graphviz import Digraph

# Flowchart of School Result Analyser
dot = Digraph('flowchart', format='png', graph_attr={'dpi': '150'})
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow', fontname='Arial')

dot.node('start', 'Start (main.py)', shape='oval', fillcolor='lightgreen')
dot.node('imp', 'import fileops, analysis\n(user-defined modules)')
dot.node('menu', 'Display Menu\nEnter choice', shape='parallelogram', fillcolor='lightblue')
dot.node('read', 'fileops.read_marks()\nRead marks.csv')
dot.node('calc', 'analysis: total, percentage,\ngrade, result')
dot.node('show', 'Display results / Search /\nToppers / Class analysis')
dot.node('add', 'Input marks (0-100)\nfileops.add_marks()\nAppend to marks.csv')
dot.node('gen', 'Generate report cards\nfileops.write_report()\nreports/report_<roll>.txt')
dot.node('view', 'View report card\nreadline(), tell(), seek(), read()')
dot.node('stop', 'Exit', shape='oval', fillcolor='lightcoral')

dot.edge('start', 'imp')
dot.edge('imp', 'menu')
dot.edge('menu', 'read', label='1, 3, 4, 5, 6')
dot.edge('read', 'calc')
dot.edge('calc', 'show', label='1, 3, 4, 5')
dot.edge('calc', 'gen', label='6')
dot.edge('menu', 'add', label='2')
dot.edge('menu', 'view', label='7')
dot.edge('menu', 'stop', label='8')
for n in ['show', 'add', 'gen', 'view']:
    dot.edge(n, 'menu', style='dashed', color='gray')

dot.render('flowchart', cleanup=True)
print("Flowchart generated as 'flowchart.png'")
