import json
def merge_json(file1, file2, output_file):

    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    
    with open(file2, 'r') as f2:
        data2 = json.load(f2)

    merged_data = {**data1, **data2}
    
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)
        
def json_union(file1_content, file2_content):
    data1 = file1_content
    data2 = file2_content

    merged_data = {**data1, **data2}
    
    return merged_data