from flask import Flask, send_file, request, jsonify
from news_graph import NewsMining
app = Flask(__name__)
from BFS import main

@app.route('/receive_json', methods=['POST'])
def receive_json():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()  
            # print("Received JSON data:", data)
            test_key="Osako"
            for i in data.keys():
                res = main(test_key)
                print(res)
            # print(res)
            file_path='graph_show.html'
            print("send file succces")
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Request must contain JSON data'}), 400

# @app.route('/send_file', methods=['GET'])
# def send_file_route():
#     try:
#         return send_file('events.json', as_attachment=True)
#     except FileNotFoundError:
#         return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
