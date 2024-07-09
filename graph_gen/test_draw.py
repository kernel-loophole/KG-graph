import json

# Load the JSON data
graph_data = """
{
    "nodes": {
        "0": {
            "label": "Quaid-e-Azam Muhammad Ali Jinnah",
            "category": "related"
        },
        "2": {
            "label": "Angela Merkel",
            "category": "related"
        },
        "4": {
            "label": "abc",
            "category": "related"
        },
        "5": {
            "label": "Elon Musk",
            "category": "related"
        },
        "7": {
            "label": "SpaceX",
            "category": "related"
        }
    },
    "edges": [
        {
            "from": "4",
            "to": "5",
            "label": "founded by",
            "category": "related"
        },
        {
            "from": "5",
            "to": "4",
            "label": "owner of",
            "category": "related"
        },
        {
            "from": "5",
            "to": "7",
            "label": "owner of",
            "category": "related"
        }
    ]
}
"""

data = json.loads(graph_data)

# Create nodes and edges data for vis.js
nodes = []
edges = []

for node_id, node_data in data['nodes'].items():
    node = {'id': node_id, 'label': node_data['label']}
    nodes.append(node)

for edge in data['edges']:
    edge = {'from': edge['from'], 'to': edge['to'], 'label': edge['label']}
    edges.append(edge)

# Create HTML content
html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Graph Visualization</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <link href="https://unpkg.com/vis-network/styles/vis-network.min.css" rel="stylesheet" type="text/css">
</head>
<body>

<div id="network"></div>

<script type="text/javascript">
  var nodes = new vis.DataSet({json.dumps(nodes)});
  var edges = new vis.DataSet({json.dumps(edges)});

  var container = document.getElementById('network');
  var data = {{
    nodes: nodes,
    edges: edges
  }};
  var options = {{
    arrows: {{
      to: {{enabled: true, scaleFactor: 1, type: 'arrow'}}
    }},
    physics: {{
      enabled: false
    }}
  }};
  var network = new vis.Network(container, data, options);
</script>

</body>
</html>
"""

# Save the HTML content to a file
with open('graph.html', 'w') as html_file:
    html_file.write(html_content)

print("HTML file generated successfully!")
