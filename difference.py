import json

with open('graph_data_from_kg.json') as f1:
	data1 = json.load(f1)

with open('graph_data.json') as f2:
	data2 = json.load(f2)

node_data1=[node for node in data2['edges']]

    # if data1['nodes'][j]['label'] in node_data1
    # if j['label'] in node_data1['label']:
    #     print(j)
# print(data1['nodes'].keys())
label_from_data_2=[]
for i in node_data1:
    print(i['label'])
    label_from_data_2.append(i['label'])
nodes={}
for count_number,j in enumerate( data1['nodes']):
    if data1['nodes'][j]['label'] in label_from_data_2:
        # print(data1['nodes'][j])
        # print(count_number)
        nodes[count_number]=data1['nodes'][j]
edges_remover=[]
nodes_inter=[]
for number,node in enumerate(data1['nodes'].values()):
    if node['label'] in label_from_data_2:
        
        nodes_inter.append(node)
    else:
        edges_remover.append(number)
edges=[]
print(edges_remover)
for j in data1['edges']:
    if j['from'] in edges_remover or j['to'] in edges_remover:
        print("removing ",j)
    else:
        edges.append(j)
# print(edges_remover)
print(edges)
node_edge=[node_edges for node_edges  in data1['edges']]

with open('diff.json', 'w') as f:
	json.dump({'nodes': nodes, 'edges': edges}, f, indent=4)

