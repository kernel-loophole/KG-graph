from news_graph import NewsMining
import threading
import pickle
tmp_event=[]
def execute_mining(data):
    Miner = NewsMining()
    Miner.main(data)
with open('news_list.pkl', 'rb') as file:
    data = pickle.load(file)
data=data[100:700]
# data=[]
# data.append(ten_ner)
sub_list=data
mining_thread = threading.Thread(target=execute_mining, args=(sub_list,))

mining_thread.start()

mining_thread.join()