import json

def ner_plotter():
    with open('graph_gen/cleaned_data.json', 'r') as f:
        data = json.load(f)

    # Convert data to vis.js format
    nodes = []
    edges = []

    node_colors = {
        "PERSON": "blue",
        "ORG": "green",
        "GPE": "red",
    }

    for node in data["nodes"]:
        node_entry = {
            "id": node['from'],
            "label": node.get("label", ""),
            "color": node_colors.get(node.get("ner", ""), "gray"),
            "category": node.get("category", ""),
            "ner": node.get("ner", "")
        }
        nodes.append(node_entry)
        node_entry = {
            "id": node['to'],
            "label": node.get("label", ""),
            "color": node_colors.get(node.get("ner", ""), "gray"),
            "category": node.get("category", ""),
            "ner": node.get("ner", "")
        }
        nodes.append(node_entry)

    # Remove duplicate nodes
    unique_nodes = {node['id']: node for node in nodes}.values()

    for edge in data["nodes"]:
        edges.append({
            "from": edge["from"],
            "to": edge["to"],
            "label": edge.get("label", ""),
            "category": edge.get("category", ""),
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

    # Fill the template with the actual data
    html_output = html_template.format(nodes=json.dumps(list(unique_nodes)), edges=json.dumps(edges))

    # Write the output to an HTML file
    with open('graph_color_output.html', 'w') as f:
        f.write(html_output)

    print("HTML file generated: graph_color_output.html")

ner_plotter()
