import json

# Load JSON data from a file
with open('graph_data.json', 'r') as file:
    data = json.load(file)

# Create a set to track seen doc_ids
seen_doc_ids = set()

# Function to check and add doc_id
def check_and_add_doc_id(item):
    doc_id = item.get('doc_id')
    if doc_id is not None:
        if doc_id in seen_doc_ids:
            return False
        seen_doc_ids.add(doc_id)
    return True

# Filter out duplicates in 'edges'
filtered_edges = []
for edge in data['edges']:
    if check_and_add_doc_id(edge):
        filtered_edges.append(edge)

# Update the data with filtered edges
data['edges'] = filtered_edges

# Save the cleaned data back to a file
with open('cleaned_data_two.json', 'w') as file:
    json.dump(data, file, indent=2)


with open('graph_data.json', 'r') as file:
    data = json.load(file)
import json

# Load the JSON data from a file
with open('cleaned_data_two.json', 'r') as file:
    data = json.load(file)

# Replace null values for 'ner' with empty strings
for edge in data.get('edges', []):
    if edge.get('ner') is None:
        edge['ner'] = ''

# Save the modified JSON back to a file
with open('cleaned_data_two.json', 'w') as file:
    json.dump(data, file, indent=2)

import json
def replace_id():
# Load JSON data from a file
    with open('cleaned_data_two.json', 'r') as file:
        data = json.load(file)

    # Create a dictionary to map edge IDs to doc_ids
    doc_id_map = {edge['id']: edge.get('doc_id', '') for edge in data['edges']}

    for edge in data['edges']:
        # if edge['label']=='Organization' or edge['label']=='Location':
        #     continue
        edge['label'] = str(doc_id_map.get(edge['id'], ''))

    # Save the updated JSON data to a new file
    with open('cleaned_data_two_final.json', 'w') as file:
        json.dump(data, file, indent=2)

    print("JSON file updated successfully.")
replace_id()