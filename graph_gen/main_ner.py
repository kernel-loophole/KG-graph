# from news_graph import NewsMining
import threading
import os
import sys
from news_graph import NewsMining

# sys.path.insert(0,'/home/haider/Desktop/sub_fol/KG-graph/news_ner')
# from news_ner import news_graph
import psycopg2

conn_params = {
    "host": "127.0.0.1",
    "database": "naas",
    "user": "postgres",
    "password": "1234"
}

try:
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()
    sql_query = "SELECT id, details FROM news_dawn;"

    cursor.execute(sql_query)
    rows = cursor.fetchall()
    rows = rows
    # print(rows)

    for row in rows:
        label_list = []
        label_id = row[0]
        details = row[1]
        # print(label_id,details)

    connection.commit()
    print("Keywords inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:

    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")

tmp_event = []


def execute_mining(data):
    Miner = NewsMining()
    NewsMining
    Miner.main(data)


def main_ner():
    # Open the pickle file in read-binary mode
    # with open('/home/haider/Desktop/sub fol/KG-graph/graph_gen/news_list.pkl', 'rb') as file:
    #     data = pickle.load(file)
    # data=rows[1]
    # data=rows[0:2]
    # print(rows[0])
    sub_list = rows[1:2]
    test_data=[(1,"In a major relief for incarcerated ex-premier and PTI founder , the Nawaz Sahraif  on Thursday set aside his physical remand in a dozen new cases over last year’s May 9 riots"),(2,"Rumours started circulating that Petitioner No. 1 Imran Khan will be shifted to the custody of Prvez Mushraf today (i.e. 25.7.2024) in connection with the very cases which form the subject matter of Writ Petition No. 45901 of 2024 and connected matters"),(3,"Imran Khan  is a Pakistani politician and former cricketer who served as the 22nd prime minister of Pakistan from August 2018 until April 2022. He is the founder and former chairman of the political party Pakistan Tehreek-e-Insaf from 1996 to 2023"),(4,"The “arrest” in these cases had come just a day after the former prime minister and his wife Bushra Bibi had been rearrested in a new Toshakhana case — following their acquittal in the Iddat case, which had them on the brink of being free from jail.")]
    print(test_data)
    # print(sub_list)
    mining_thread = threading.Thread(target=execute_mining, args=(test_data,))
    mining_thread.start()

    mining_thread.join()


main_ner()
