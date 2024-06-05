import json
import networkx as nx
import matplotlib.pyplot as plt

with open('diff.json', 'r') as f:
    graph_data = json.load(f)

G = nx.DiGraph()

for node_id, node_data in graph_data['nodes'].items():
    G.add_node(node_id, label=node_data['label'], category=node_data['category'])

for edge in graph_data['edges']:
    G.add_edge(str(edge['from']), str(edge['to']), label=edge['label'], category=edge['category'])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels={node: data['label'] for node, data in G.nodes(data=True)}, node_size=5000, node_color="skyblue", font_size=10, font_weight="bold")
edge_labels = {(from_node, to_node): data['label'] for from_node, to_node, data in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# Show the graph
plt.title('Graph Visualization')
plt.show()
