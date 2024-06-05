from news_graph import NewsMining
test_str_1="Pakistan was founded by Quaid-e-Azam Muhammad Ali Jinnah in 1947."
test_string_one="Quaid-e-Azam Muhammad Ali Jinnah was good man"
long_sen="The government has already achieved a Rs60 per litre petroleum levy — the maximum permissible limit under the law — on both petrol and HSD. The government had set a budget target to collect Rs869 billion as a petroleum levy during the current fiscal year under the commitments made with the International Monetary Fund (IMF) but was hoping the collection to go beyond Rs950bn by the end of June."
# test_fail="The bank is on the river, and the bank approved my loan application."
ten_ner="In 2022, John Smith, the CEO of XYZ Corporation, attended the United Nations General Assembly in New York City, where he discussed climate change with Angela Merkel, the Chancellor of Germany.He highlighted the company's partnership with SpaceX to Angela Merkel, headed by Elon Musk, to develop innovative sustainable energy solutions for the future.Quaid-e-Azam Muhammad Ali Jinnah was good man.He was born in Karachi.He founded abc with elon musk.he was good friend of Elon Musk"
test_str='''
Iranian President Ebrahim Raisi arrived in Lahore on Tuesday morning and visited Allama Iqbal’s mausoleum.

Punjab Chief Minister Maryam Nawaz received Raisi and his delegation at the Allama Iqbal International Airport on the second day of his three-day official visit. His visit to Pakistan is the first of its kind by any head of state after the February 8 general elections.


According to PTV News, Punjab Chief Secretary Zahid Akthar Zaman, Inspector General of Police Dr Usman Anwar and Iranian consul general in Lahore Mehran Movahhedfar were among those receiving him.

Senior provincial minister Marriyum Aurangzeb, Senator Pervaiz Rasheed and provincial ministers Uzma Bukhari, Mujtuba Shujaur Rehman, Khawaja Sulaiman Rafiq, Bilal Yasin, and Chaudhry Shafay Hussain were also present on the occasion.

The Iranian president then paid a visit to Allama Iqbal’s mausoleum, where he laid a floral wreath and offered fateha.

Raisi visits Allama Iqbal mausoleum in Lahore. — DawnNewsTV
Speaking on the occasion, Raisi said he did not “feel like a stranger at all”, adding that there were “special emotions and connections” with Pakistani people that kept the two nations connected.

“I wanted that a public rally be held so I could address the public but due to some reasons, the conditionalities were such that it could not be made possible,” he said.

“On behalf of the supreme leader of the Islamic Republic of Iran, I say my greetings to the people of Pakistan and Lahore,” Raisi said, appreciating the “revolutionary spirit” present in the people here.

The Iranian president highlighted that Allama Iqbal was an extremely important personality for Iran as he was a very inspirational person.

The Foreign Office (FO) had stated earlier that Raisi would visit Lahore and Karachi and meet with the provincial leadership.

The Punjab government and Sindh governments have announced local holidays today (Tuesday) in the Lahore district and Karachi division, respectively, to “avoid the consequent inconvenience to the general public” ahead of the visit of foreign dignitaries, including Raisi. The Sindh government has also imposed a complete ban on drones in Karachi division from April 22 to April 28.'''
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
with open('news_list.pkl', 'rb') as file:
    data = pickle.load(file)
data=data[100:700]
# data=[]
# data.append(ten_ner)
sub_list=data
mining_thread = threading.Thread(target=execute_mining, args=(sub_list,))

mining_thread.start()

mining_thread.join()