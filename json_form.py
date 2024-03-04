import json

def format_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            formatted_json = json.dumps(json_data, indent=2)
            with open(file_path, 'w') as output_file:
                output_file.write(formatted_json)
            
            return formatted_json
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except json.JSONDecodeError:
        return f"Invalid JSON format in file: {file_path}"

file_path = 'graph_data.json'  
formatted_data = format_json_file(file_path)

# if formatted_data:
#     print(formatted_data)
#     print(f"Formatted JSON data has been written to: {file_path}")
# else:
#     print("Error occurred while processing the JSON file.")
