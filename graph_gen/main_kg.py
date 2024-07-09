from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import matplotlib.pyplot as plt
import networkx as nx
import json
import pickle
import psycopg2
import sys
sys.path.append('/home/pcn/Desktop/NAaS/know')
# from news_graph import NewsMining

# Initialize NewsMining
# Miner = NewsMining()

# Database connection information
conn_params = {
    "host": "127.0.0.1",
    "database": "naas",
    "user": "postgres",
    "password": "1234"
}

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(**conn_params)
    cursor = connection.cursor()

    # SQL query to fetch IDs from the table
    sql_query = "SELECT id, details FROM news_dawn;"

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all rows from the result
    rows = cursor.fetchall()
    rows=rows
    # print(rows)
    # cursor.execute("SELECT * from keywords;")
    # tables=cursor.fetchall()
    # print(tables)
    # # Process each row
    for row in rows:
        label_list = []
        label_id = row[0]
        details = row[1]

        # Obtain keywords using NewsMining
        # try:
        #     # data = Miner.main(details)
        #     # print(data)
        #     for label in data['edges']:
        #         label_list.append(label['label'])
        # except Exception as err:
        #     pass
            # print(err)
        # for keyword in label_list:
        #     sql_insert = "INSERT INTO keywords (word, dawn_id) VALUES (%s,%s);"
        #     cursor.execute(sql_insert, (keyword, label_id))

    # # Commit the transaction
    connection.commit()
    # check_query="SELECT * from keywords;"
    # cursor.execute(check_query)
    # check_row=cursor.fetchall()
    # print(check_row)
    print("Keywords inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
ten_ner="In 2022, John Smith, the CEO of XYZ Corporation, attended the United Nations General Assembly in New York City, where he discussed climate change with Angela Merkel, the Chancellor of Germany.He highlighted the company's partnership with SpaceX to Angela Merkel, headed by Elon Musk, to develop innovative sustainable energy solutions for the future.Quaid-e-Azam Muhammad Ali Jinnah was good man.He was born in Karachi.He founded abc with elon musk.he was good friend of Elon Musk"
long_sen="The government has already achieved a Rs60 per litre petroleum levy — the maximum permissible limit under the law — on both petrol and HSD. The government had set a budget target to collect Rs869 billion as a petroleum levy during the current fiscal year under the commitments made with the International Monetary Fund (IMF) but was hoping the collection to go beyond Rs950bn by the end of June."
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
def extract_relations_from_model_output(text):
    relations = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        relations.append({
            'head': subject.strip(),
            'type': relation.strip(),
            'tail': object_.strip()
        })
    return relations

# knowledge base class
class KB():
    def __init__(self):
        self.relations = []

    def are_relations_equal(self, r1, r2):
        return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])

    def exists_relation(self, r1):
        return any(self.are_relations_equal(r1, r2) for r2 in self.relations)

    def add_relation(self, r):
        if not self.exists_relation(r):
            self.relations.append(r)
    def print(self):
        re_list=[]
        for r in self.relations:
            # print(f"  {r}")
            re_list.append(r)
        return re_list
def from_small_text_to_kb(text, verbose=False):
    kb = KB()
    model_inputs = tokenizer(text,  padding=True, truncation=True,
                            return_tensors='pt')
    if verbose:
        print(model_inputs)
    gen_kwargs = {
        "max_length": 520,
        "length_penalty": 11,
        "num_return_sequences": 3
    }
    generated_tokens = model.generate(
        **model_inputs,
        **gen_kwargs,
    )
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)
    for sentence_pred in decoded_preds:
        relations = extract_relations_from_model_output(sentence_pred)
        for r in relations:
            kb.add_relation(r)

    return kb
def main_kg():
    tmp_event = []
    data = rows[0:15]
    # print(data)
    label_ids = [row[0] for row in data]
    details = [row[1] for row in data]
    
    relations_find_all = []
    for i in range(len(data)):
        kb = from_small_text_to_kb(details, verbose=True)
        # kb.print()
        relations = kb.print()
        for j in relations:
            relations_find_all.append(j)
    print(relations_find_all)
    G = nx.DiGraph()
    graph_data = {
        "nodes": {},
        "edges": []
    }

    node_ids = {}
    node_id_counter = 0

    for rel in relations_find_all:
        head = rel['head']
        tail = rel['tail']
        rel_type = rel['type']
        label_id = rel['label_id']  # Assuming 'label_id' is included in relation dictionary

        if head not in node_ids:
            node_ids[head] = node_id_counter
            node_id_counter += 1
        if tail not in node_ids:
            node_ids[tail] = node_id_counter
            node_id_counter += 1
        if node_ids[head] not in graph_data["nodes"]:
            graph_data["nodes"][node_ids[head]] = {"label": head, "category": "related"}
        if node_ids[tail] not in graph_data["nodes"]:
            graph_data["nodes"][node_ids[tail]] = {"label": tail, "category": "related"}
        graph_data["edges"].append({
            "from": node_ids[head], 
            "to": node_ids[tail], 
            "label": rel_type, 
            "category": "related",
            "id": label_id
        })

    with open('graph_data_from_kg.json', 'w') as json_file:
        json.dump(graph_data, json_file, indent=4)

    print("Graph data has been stored in graph_data_from_kg.json")

    for relation in relations_find_all:
        G.add_edge(relation['head'], relation['tail'], relation_type=relation['type'])


main_kg()