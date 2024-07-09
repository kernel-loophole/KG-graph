import json
import networkx as nx
import matplotlib.pyplot as plt


with open('graph_data.json', 'r') as file:
    data = json.load(file)

import networkx as nx
import matplotlib.pyplot as plt

class GraphShow:
    def __init__(self):
        pass

    def create_graph(self, data_nodes, data_edges):
        G = nx.DiGraph()

        # Add nodes
        for node in data_nodes:
            G.add_node(node["id"], label=node["label"], category=node["category"], ner=node.get("ner"), value=node.get("value"))

        # Add edges
        for edge in data_edges:
            G.add_edge(edge["from"], edge["to"], label=edge["label"], category=edge["category"])

        return G

    def draw_graph(self, G):
        pos = nx.spring_layout(G, seed=42)  # Use spring_layout with a fixed seed for reproducibility
        node_labels = nx.get_node_attributes(G, 'label')
        edge_labels = nx.get_edge_attributes(G, 'label')

        node_colors = [self.get_node_color(node["category"]) for node in G.nodes.values()]
        edge_colors = [self.get_edge_color(edge["category"]) for edge in G.edges.values()]

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, cmap=plt.cm.Blues)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowsize=20, connectionstyle="arc3,rad=0.1")

        plt.show()

    def get_node_color(self, category):
        if category == 'frequency':
            return 'lightblue'
        elif category == 'keyword':
            return 'lightgreen'
        elif category == 'related':
            return 'lightcoral'
        elif category == 'Organization':
            return 'red'
        elif category == 'Location':
            return 'black'
        else:
            return 'blue'

    def get_edge_color(self, category):
        if category == 'frequency':
            return 'blue'
        elif category == 'keyword':
            return 'green'
        elif category == 'related':
            return 'red'
        else:
            return 'gray'


graph_show = GraphShow()
data_nodes = data['edges']  # Replace with your actual data
data_edges = data['nodes']  # Replace with your actual data
G = graph_show.create_graph(data_nodes, data_edges)
graph_show.draw_graph(G)
