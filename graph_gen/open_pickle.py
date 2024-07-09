import pickle

# File path of the pickle file
file_path = 'data.pkl'

# Open the pickle file in read-binary mode
with open(file_path, 'rb') as file:
    # Load the Python object from the pickle file
    loaded_data = pickle.load(file)

# Now you can use the loaded_data object
print(loaded_data)