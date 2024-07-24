import json
def ner_finder():
    with open('graph_gen/graph_data.json', 'r') as file:
        file_one_data = json.load(file)

    with open('diff.json', 'r') as file:
        file_two_data = json.load(file)


    ner_mapping = {}
    for node in file_one_data['edges']:
        ner_mapping[node['label']] = node['ner']

    print(ner_mapping)
    for node_id, node_data in file_two_data['nodes'].items():
        label = node_data['label']
        if label in ner_mapping:
            print(label)
            file_two_data['nodes'][node_id]['ner'] = ner_mapping[label]
            

    with open('updated_file_two_final.json', 'w') as file:
        json.dump(file_two_data, file, indent=4)
