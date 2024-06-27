from graphviz import Digraph

# Creare grafic direcționat nou pentru diagrama UML de stări
dot = Digraph('UMLStateDiagram', comment='Diagramă de stări pentru GUI')

# Definire stări
dot.node('A', 'MainMenuPage', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('B', 'GoWindow', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('C', 'BvBController', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('D', 'PvBController', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('E', 'GameSetup', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('F', 'GamePlay', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('G', 'GameOver', shape='ellipse', style='filled', fillcolor='lightcoral')

# Definire muchii cu etichete pentru tranzițiile între stări
dot.edge('A', 'B', 'Start Game')
dot.edge('B', 'C', 'Bot vs Bot')
dot.edge('B', 'D', 'Player vs Bot')
dot.edge('B', 'E', 'Setup Game')
dot.edge('C', 'F', 'Start Simulation')
dot.edge('D', 'F', 'Player Move')
dot.edge('F', 'G', 'End Game')
dot.edge('G', 'A', 'Back to Menu')

# Redare grafic în fișier
output_path = 'uml_state_diagram_gui.png'
dot.render(output_path, format='png', cleanup=False)

print(f"Diagrama a fost salvată ca {output_path}")
