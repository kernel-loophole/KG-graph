import json

# Read data from JSON file
with open('updated_file_two_final.json', 'r') as f:
    data = json.load(f)

# Convert data to vis.js format
nodes = []
edges = []

node_colors = {
    "PERSON": "blue",
    "ORG": "green",
    "GPE":"red",
}

for node_id, node_data in data["nodes"].items():
    node_id = int(node_id)
    node = {
        "id": node_id,
        "label": node_data["label"],
        "color": node_colors.get(node_data.get("ner", ""), "gray"),
        "category": node_data["category"],
        "ner": node_data.get("ner", "")
    }
    nodes.append(node)

for edge in data["edges"]:
    edges.append({
        "from": edge["from"],
        "to": edge["to"],
        "label": edge["label"],
        "category": edge["category"],
        "arrows": "to"
    })

# Generate HTML and JavaScript for vis.js
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Graph</title>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.css" rel="stylesheet" type="text/css">
    <style type="text/css">
        #mynetwork {{
            width: 100%;
            height: 800px;
            border: 1px solid lightgray;
        }}
    </style>
</head>
<body>

<div id="mynetwork"></div>

<script type="text/javascript">
    var nodes = new vis.DataSet({nodes});
    var edges = new vis.DataSet({edges});

    var container = document.getElementById('mynetwork');
    var data = {{
        nodes: nodes,
        edges: edges
    }};
    var options = {{
        nodes: {{
            shape: 'dot',
            size: 20,
            font: {{
                size: 15,
                color: '#000000'
            }},
            borderWidth: 2
        }},
        edges: {{
            width: 2,
            font: {{
                size: 12,
                align: 'middle'
            }},
            arrows: {{
                to: {{enabled: true, scaleFactor: 1}}
            }},
            smooth: {{
                enabled: true,
                type: 'dynamic'
            }}
        }},
        physics: {{
            enabled: true
        }}
    }};
    var network = new vis.Network(container, data, options);
</script>

</body>
</html>
"""

html_output = html_template.format(nodes=json.dumps(nodes), edges=json.dumps(edges))


with open('graph_color_put.html', 'w') as f:
    f.write(html_output)

print("HTML file generated: graph.html")
