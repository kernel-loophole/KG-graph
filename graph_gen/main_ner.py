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
    sub_list = rows[0:5]
    # print(sub_list)
    mining_thread = threading.Thread(target=execute_mining, args=(sub_list,))
    mining_thread.start()

    mining_thread.join()


main_ner()
