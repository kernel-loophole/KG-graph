from news_graph import NewsMining
test_str_1="Pakistan was founded by Quaid-e-Azam Muhammad Ali Jinnah in 1947."
test_string_one="Quaid-e-Azam Muhammad Ali Jinnah was good man"
long_sen="The government has already achieved a Rs60 per litre petroleum levy — the maximum permissible limit under the law — on both petrol and HSD. The government had set a budget target to collect Rs869 billion as a petroleum levy during the current fiscal year under the commitments made with the International Monetary Fund (IMF) but was hoping the collection to go beyond Rs950bn by the end of June."
# test_fail="The bank is on the river, and the bank approved my loan application."
ten_ner="In 2022, John Smith, the CEO of XYZ Corporation, attended the United Nations General Assembly in New York City, where he discussed climate change with Angela Merkel, the Chancellor of Germany.He highlighted the company's partnership with SpaceX to Angela Merkel, headed by Elon Musk, to develop innovative sustainable energy solutions for the future.Quaid-e-Azam Muhammad Ali Jinnah was good man.He was born in Karachi.He founded abc with elon musk.he was good friend of Elon Musk"
# import threading
# import pickle
# def execute_mining(data):
#     Miner = NewsMining()
#     Miner.main(data)

# # Open the pickle file in read-binary mode
# with open('news_list.pkl', 'rb') as file:
#     data = pickle.load(file)
# sub_list=data
# mining_thread = threading.Thread(target=execute_mining, args=(sub_list,))

# # Start the thread
# mining_thread.start()

# mining_thread.join()
import threading
import pickle
tmp_event=[]
# Define the function to execute mining
# def execute_mining(data):
#     Miner = NewsMining()
#     events=Miner.main(data)
#     tmp_event.append(events)
#     # print(events)
# with open('news_list.pkl', 'rb') as file:
#     data = pickle.load(file)
# data=data[0:500]
# batch_size = 100  
# num_batches = (len(data) + batch_size - 1) // batch_size
# batches = [data[i * batch_size:(i + 1) * batch_size] for i in range(num_batches)]
# threads = []
# for batch in batches:
#     mining_thread = threading.Thread(target=execute_mining, args=(batch,))
#     threads.append(mining_thread)
#     mining_thread.start()
# for thread in threads:
#     thread.join()
# with open('data.pkl', 'wb') as file:
#     pickle.dump(tmp_event, file)
def execute_mining(data):
    Miner = NewsMining()
    Miner.main(data)

# Open the pickle file in read-binary mode
# with open('news_list.pkl', 'rb') as file:
#     data = pickle.load(file)
data=[]
data.append(ten_ner)
sub_list=data
mining_thread = threading.Thread(target=execute_mining, args=(sub_list,))

mining_thread.start()

mining_thread.join()