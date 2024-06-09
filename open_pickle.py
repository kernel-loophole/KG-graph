import pickle
file_path = 'data.pkl'


with open(file_path, 'rb') as file:
    loaded_data = pickle.load(file)
print(loaded_data)