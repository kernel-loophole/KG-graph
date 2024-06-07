import json


class GraphShow():
    """Create demo page"""

    def __init__(self):
        self.base = '''
    <html>
    <head>
      <script type="text/javascript" src="VIS/dist/vis.js"></script>
      <link href="VIS/dist/vis.css" rel="stylesheet" type="text/css">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>

    <div id="VIS_draw"></div>

    <script type="text/javascript">
      var nodes = data_nodes;
var edges = data_edges;

var container = document.getElementById("VIS_draw");

var data = {
  nodes: nodes,
  edges: edges
};
console.log(data);
var options = {
  nodes: {
    shape: 'circle',
    font: {
      size: 15
    }
  },
  edges: {
    font: {
      size: 10,
      align: 'center'
    },
    arrows: {
      to: { enabled: true, scaleFactor: 1.2 }
    },
    smooth: { enabled: true }
  },
  physics: {
    enabled: true
  }
};

data.nodes.forEach(function (node) {
  if (node.category === 'frequency') {
    node.color = 'lightblue';
  } else if (node.category === 'keyword') {
    node.color = 'lightgreen';
  } 
  else if (node.category === 'Organization') {
    node.color = 'red';
  }else if (node.category === 'Location') {
    node.color = 'black';
  }else if (node.category === 'related') {
    node.color = 'lightcoral';
  } 
  // Set a common size for all nodes
});

data.nodes.forEach(function (node) {
  // Adjust node color based on value from result_dic
  if (node.value) {
    // Assuming result_dic values are in the range [0, 1]
    var hue = Math.floor((1 - node.value) * 120); // Adjust hue based on value
    node.color = 'lightyellow';
  }
});

data.edges.forEach(function (edge) {
  if (edge.category === 'frequency') {
    edge.color = { color: 'blue' };
  } else if (edge.category === 'keyword') {
    edge.color = { color: 'green' };
  } else if (edge.category === 'related') {
    edge.color = { color: 'red' };
  } else {
    edge.color = { color: 'black' };
  }
});

var network = new vis.Network(container, data, options);


    </script>
    </body>
    </html>
    '''

    def create_html(self, data_nodes, data_edges):
        """Generate html file"""
        f = open('graph_show_id.html', 'w+')
        print(data_edges)
        html = self.base.replace('data_nodes', str(data_nodes)).replace('data_edges', str(data_edges))
        f.write(html)
        f.close()

    def return_edge(self, events, result_dic):
        with open('graph_data.json', 'r') as f:
            data = json.load(f)
        data_nodes = data['edges']
        # test_lable=[i for i in data_nodes['label']]
        test_lable = {}
        for i in data_nodes:
            # print(i['doc_id'])
            #label plot from JSON file
            try:
                test_lable[i['label']] = i['content']
            except:
                pass
        """Read data and values"""
        nodes = []
        # for event in events:
        #     nodes.append(event[0])
        #     nodes.append(event[1])
        #     print(f"Node: {event[0]}, Index: {index * 2}")
        #     print(f"Node: {event[1]}, Index: {index * 2 + 1}")
        for index, event in enumerate(events):
            nodes.append(event[0])
            nodes.append(event[1])
            # print(f"Node: {event[0]}, Index: {index * 2}")
            # print(f"Node: {event[1]}, Index: {index * 2 + 1}")
        # print(nodes)
        node_dict = {node: index for index, node in enumerate(nodes)}
        # print(node_dict)
        data_nodes = []
        data_edges = []
        for node, id in node_dict.items():
            if node in test_lable.keys():
                print("~~~~~~~~~~~",node)
                print("~~~~~~~~~~~~~~~~~~",test_lable)
                node_x = str(test_lable[node])
                data = {
                "label": node_x,
                "category": 'frequency' if 'frequency' in node else 'keyword' if 'keyword' in node else 'related' if 'related' in node else 'Organization' if 'Organization' in node else 'Location' if 'Location' in node else 'other',
                "ner": "PERSON" if "PERSON" in node else "org",
                "value": result_dic.get(node, 0),  # Get value from result_dic, default to 0 if not present
                'id': id
            }
            else:
                data = {
                    "label": node,
                    "category": 'frequency' if 'frequency' in node else 'keyword' if 'keyword' in node else 'related' if 'related' in node else 'Organization' if 'Organization' in node else 'Location' if 'Location' in node else 'other',
                    "ner": "PERSON" if "PERSON" in node else "org",
                    "value": result_dic.get(node, 0),  # Get value from result_dic, default to 0 if not present
                    'id': id
                }

            data_nodes.append(data)
        # print(events)
        for edge in events:
            print(node_dict.get(edge[1]))
            data = {
                'from': node_dict.get(edge[0]),
                'label': '',
                'to': node_dict.get(edge[1]),
                'category': 'frequency' if 'frequency' in edge else 'keyword' if 'keyword' in edge else 'related' if 'related' else 'Organization' if 'Organization' in node in edge else 'Location' if 'Location' in node else 'other'
            }

            data_edges.append(data)
        # print(data_nodes,data_edges)
        self.create_html(data_nodes, data_edges)
        return data_edges, data_nodes

    def create_page(self, events, result_dic):
        """Read data and values, assign edge and node colors based on categories and values"""
        nodes = {}


        for event in events:
            nodes[event[0]] = event[1]

        node_dict = nodes

        data_nodes = []
        data_edges = []
        # print(node_dict)
        for node, id in node_dict.items():
            # print(node)

            category = 'frequency' if 'frequency' in id else 'keyword' if 'keyword' in id else 'related' if 'related' in id else 'Organization' if 'Organization' in id else 'Location' if 'Location' in node else 'other'

            data = {
                "id": id,
                "label": node,
                "color": {'background': self.get_node_color(category), 'border': 'black'},
                "value": result_dic.get(node, 0)  # Get value from result_dic, default to 0 if not present
            }

            data_nodes.append(data)

        for edge in events:
            category = 'frequency' if 'frequency' in edge else 'keyword' if 'keyword' in edge else 'related' if 'related' in edge else 'other'
            data = {
                'from': node_dict.get(edge[0]),
                'label': '',
                'to': node_dict.get(edge[1]),
                'color': {'color': self.get_edge_color(category)}
            }

            data_edges.append(data)

        self.create_html(data_nodes, data_edges)
        return

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
test=GraphShow()
with open('cleaned_data_two.json', 'r') as f:
    data = json.load(f)

test.create_html(data['edges'],data['nodes'])