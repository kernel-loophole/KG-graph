import json
from queue import Queue
import threading
from graph_show import GraphShow
from news_graph import NewsMining

class GraphProcessor:
    def __init__(self, json_file):
        self.graph = self.build_graph_from_json(json_file)

    def build_graph_from_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        graph = {}
        for node in data['edges']:
            node_id = node.get('id')
            graph[node_id] = []
        for edge in data['nodes']:
            from_node = edge.get('from')
            to_node = edge.get('to')
            if from_node is not None and to_node is not None:
                if from_node not in graph:
                    graph[from_node] = []
                graph[from_node].append(to_node)
        return graph

    def bfs_related_nodes(self, keyword):
        visited = set()
        result = []
        re = read_json_file("query_graph.json")

        for start_node in self.graph:
            if str(keyword) in str(start_node) and start_node not in visited:
                queue = Queue()
                queue.put((start_node, 0))  # Tuple (node, distance)
                visited.add(start_node)
                re = read_json_file("query_graph.json")

                while not queue.empty():
                    current_node, distance = queue.get()
                    result.append(current_node)

                    for edge in re['edges']:
                        if current_node == edge['id']:
                            edge['distance'] = distance

                    for neighbor in self.graph.get(current_node, []):
                        if neighbor not in visited:
                            queue.put((neighbor, distance + 1))
                            visited.add(neighbor)

                            for edge in re['edges']:
                                if edge['id'] == neighbor:
                                    edge['distance'] = distance + 1

        with open('query_graph.json', 'w') as json_file:
            json.dump(re, json_file, indent=2)
        result_one = {}
        re = read_json_file("query_graph.json")

        for edge in re['edges']:
            if edge['distance'] > 0:
                result_one[edge['label']] = edge['distance']

        if len(result_one) < 1:
            return None
        final_distance = dict(sorted(result_one.items(), key=lambda item: item[1]))

        return final_distance

    def get_labels_by_ids(self, node_ids):
        labels = []
        for node_id in node_ids:
            for edge in self.graph:
                if 'id' in edge and edge['id'] == node_id:
                    labels.append(edge['label'])
                    break
        return labels

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except json.JSONDecodeError:
        return f"Invalid JSON format in file: {file_path}"

def find_matching_id(json_data, keyw):
    nodes_id = json_data['edges']
    for i in nodes_id:
        if i['label'] == keyw:
            return i['id']

def process_data(search_keyword):
    processor = GraphProcessor('graph_data.json')
    re = read_json_file("graph_data.json")
    search_key = search_keyword
    ids = processor.bfs_related_nodes(find_matching_id(re, search_key))
    test_json = read_json_file('graph_data.json')
    nodes_data = test_json['edges']
    egdes_dat = test_json['nodes']
    test_nodes_data = []

    for i in nodes_data:
        try:
            if i['label'] in ids:
                print("found")
                print(i['label'])
                test_nodes_data.append(i)
        except:
            pass
    data = {'nodes': egdes_dat, "edges": test_nodes_data}
    with open("test_json.json", 'w') as file:
        json.dump(data, file)

    # format_json_file('test_json.json')
    with open('events.json', 'r') as file:
        events = json.load(file)
    with open('result_dic.json', 'r') as file:
        result_dic = json.load(file)
    with open('test_json.json', 'r') as file:
        data = json.load(file)
    labels = []
    tmp_event = []
    Ner_data = {"Person": 0, "Location": 0, "Organization": 0}
    labels.append(search_key)
    test_data = []

    for i in data['edges']:
        labels.append(i['label'])

    # for k, i in enumerate(events):
    #     if i[0] in labels:
    #         if i[1] == "Organization":
    #             Ner_data['Organization'] += 1
    #         if i[1] == "Location":
    #             Ner_data['Location'] += 1
    #         if i[1] == "Person":
    #             Ner_data['Person'] += 1
    #     else:
    #         pass

    org_count = 0
    for k, i in enumerate(events):
        if i[0] in labels:
            if i[1] not in Ner_data.keys():
                continue
            labels.remove(i[0])
            tmp_event.append(i)
            tmp_dir_ner = []

            if org_count < 3:
                if i[1] == "Organization":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Person')
                    tmp_event.append(tmp_dir_ner)
                    org_count += 1
                if i[1] == "Location":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Person')
                    tmp_event.append(tmp_dir_ner)
                    org_count += 1
                if i[1] == "Person":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Location')
                    tmp_event.append(tmp_dir_ner)
                    org_count += 1

    test_grp = GraphShow()
    print(tmp_event)
    tmp_dir = {}
    test_grp.create_page(tmp_event, result_dic)
    nodes, edge = test_grp.return_edge(tmp_event, result_dic)
    return tmp_event, result_dic

def main(search_keyword):
    ev = NewsMining()
    t1 = threading.Thread(target=process_data, args=(search_keyword,))
    t1.start()

if __name__ == "__main__":
    main("the Punjab Assembly")
