import json
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
    #get the links for json
    sql_query_link = "SELECT id,link FROM news_dawn;"
    cursor.execute(sql_query_link)
    links = cursor.fetchall()
    links = links
    connection.commit()
    print("Keywords inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:

    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")

# Load the JSON file
with open('cleaned_data_two_final.json', 'r') as f:
    data = json.load(f)

# List of tuples with doc_id and corresponding link
# links = [
#     (1, 'https://www.dawn.com/news/1748919/worlds-glaciers-melted-at-dramatic-speed-in-2022-un'),
#     (2, 'https://www.dawn.com/news/1748923/pakistans-state-run-firms-worst-in-asia'),
#     (3, 'https://www.dawn.com/news/1748921/basmati-rice-exports-surge-45pc-in-march'),
#     (4, 'https://www.dawn.com/news/1748938/pti-chief-to-rethink-tickets-to-pacify-unhappy-aspirants'),
#     (5, 'https://www.dawn.com/news/1748935/pm-concerned-for-safety-of-citizens-in-sudan'),
#     (6, 'https://www.dawn.com/news/1748931/in-standoff-with-judiciary-pm-shehbaz-stands-firm-on-parliaments-supremacy'),
#     (7, 'https://www.dawn.com/news/1748930/analysis-why-the-judicial-indifference-towards-kp-polls'),
#     (8, 'https://www.dawn.com/news/1748910/security-beefed-up-at-all-jails-in-sindh'),
#     (9, 'https://www.dawn.com/news/1748899/intercity-transporters-warned'),
#     (20, 'https://www.dawn.com/news/1748923/pakistans-state-run-firms-worst-in-asia'),
#     (10, 'https://www.dawn.com/news/1748897/shikarpur-judge-remands-ali-amin-gandapur-in-judicial-custody-till-25th'),
#     (11, 'https://www.dawn.com/news/1748896/unusual-rise-in-preventable-diseases-among-children-in-flood-hit-areas'),
#     (12, 'https://www.dawn.com/news/1748894/ppp-believes-in-dialogue-but-allies-think-differently-says-murad-ali-shah'),
#     (13, 'https://www.dawn.com/news/1748893/three-killed-four-injured-in-road-accident'),
#     (14, 'https://www.dawn.com/news/1748941/condemned-on-television'),
#     (15, 'https://www.dawn.com/news/1748939/initial-figures-of-census-put-countrys-population-at-235m'),
#     (16, 'https://www.dawn.com/news/1748937/president-alvi-pm-shehbaz-ask-people-to-shun-differences-assure-nation-of-good-days'),
# ]

# Convert list of tuples into a dictionary for faster lookup
link_dict = dict(links)

# Iterate over the edges and add the corresponding link if the 'from' key exists in link_dict
for edge in data['edges']:
    try:
        doc_id = edge['doc_id']
        if doc_id in link_dict:
            edge['link'] = link_dict[doc_id]
    except:
        pass
# Save the updated JSON back to a file
with open('updated_file_with_links_final.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Updated JSON file with links has been saved.")
