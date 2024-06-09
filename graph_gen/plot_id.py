import json
import networkx as nx
import plotly.graph_objects as go

# Load the JSON data from the file
with open('cleaned_data.json', 'r') as f:
    data = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph and keep track of node labels
node_labels = {}
for node in data['nodes']:
    G.add_edge(node['from'], node['to'])
for edge in data['edges']:
    from_node = edge['label']
    to_node = edge['label']
    node_labels[edge['id']] = edge['label']
# Generate positions for all nodes using spring layout
pos = nx.spring_layout(G)
# Create a Plotly figure
fig = go.Figure()

# Add edges to the figure
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    fig.add_trace(go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        mode='lines',
        line=dict(width=2, color='blue'),
        hoverinfo='none'
    ))

# Add nodes to the figure with labels
for node in G.nodes():
    x, y = pos[node]
    label = node_labels.get(node, str(node))
    if label in node_labels.values():
        print(label)
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(size=10, color='red'),
            text=[label],
            textposition='top center',
            hoverinfo='text'
        ))

# Update layout of the figure
fig.update_layout(
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

# Show the figure
fig.show()
