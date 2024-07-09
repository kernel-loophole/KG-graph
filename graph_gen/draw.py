import json

# Read JSON file
with open('diff.json', 'r') as file:
    data = json.load(file)

# Prepare nodes and edges data for vis.js
nodes = [{'id': node_id, 'label': node_data['label']} for node_id, node_data in data['nodes'].items()]
edges = [{'from': str(edge['from']), 'to': str(edge['to']), 'label': edge['label']} for edge in data['edges']]

# Generate HTML code
html_code = f"""<!doctype html>
<html>
<head>
  <title>Graph from JSON Data</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style type="text/css">
    body, html {{
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }}
    #mynetwork {{
      width: 100%;
      height: 100%;
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
    autoResize: true,
    nodes: {{

      font: {{
        size: 15
      }}
    }},
     smooth: {{ enabled: true }},
     
    edges: {{
      arrows: 'to'
    }},
    physics: {{
      enabled: false,
      hierarchicalRepulsion: {{
        nodeDistance: -3000
      }}
    }}
  }};
  
  var network = new vis.Network(container, data, options);
</script>
</body>
</html>
"""

html_code = html_code.replace('{json_nodes}', json.dumps(nodes))
html_code = html_code.replace('{json_edges}', json.dumps(edges))

with open('graph.html', 'w') as file:
    file.write(html_code)
