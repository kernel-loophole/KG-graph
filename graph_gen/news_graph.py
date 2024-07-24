import re
from collections import Counter
import spacy
import pickle
import json
import uuid
from tqdm import tqdm
# from BFS import read_json_file
# from graph_show import GraphShow
# from graph_show import GraphShow
# from news_graph import GraphShow
import graph_show
# from text rank import TextRank
import textrank
# from text rank import TextrankGraph
# from json_form import format_json_file
import json_form

# from BFS import GraphProcessor

nlp = spacy.load('en_core_web_lg')


def combination(a):
    '''list all combination'''
    combines = []
    if len(a) == 0:
        return []
    for i in a:
        for j in a:
            if i == j:
                continue
            combines.append('@'.join([i, j]))
    # print(combines)
    return combines


def collect_coexist(ner_sents, ners):
    """Construct NER co-occurrence matrices"""
    co_list = []
    for words in ner_sents:
        co_ners = set(ners).intersection(set(words))
        # print(co_ners)

        co_info = combination(list(co_ners))
        co_list += co_info
    if not co_list:
        return []
    #co occurence on the base on of intersection
    return {i[0]: i[1] for i in Counter(co_list).most_common()}


def build_parse_chile_dict(sent, tuples):
    child_dict_list = list()
    for word in sent:
        child_dict = dict()
        for arc in tuples:
            if arc[3] == word:
                if arc[-1] in child_dict:
                    child_dict[arc[-1]].append(arc)
                else:
                    child_dict[arc[-1]] = []
                    child_dict[arc[-1]].append(arc)
        child_dict_list.append([word, word.pos_, word.i, child_dict])
    return child_dict_list


def syntax_parse(sent):
    """Convert one sentence to conll format."""
    tuples = list()
    for word in sent:
        if word.head is word:
            head_idx = 0
        else:
            head_idx = word.head.i + 1
        tuples.append([word.i + 1,  # Current word index, begin with 1
                       word.text,  # Word
                       word.pos_,  # Coarse-grained tag
                       word.head,
                       head_idx,  # Head of current  Index
                       word.dep_,  # Relation
                       ])
    return tuples


def conll_syntax(sent):
    """Convert one sentence to conll format."""

    tuples = list()
    for word in sent:
        if word.head is word:
            head_idx = 0
        else:
            head_idx = word.head.i + 1
        tuples.append([word.i + 1,  # Current word index, begin with 1
                       word.text,  # Word
                       word.lemma_,  # Lemma
                       word.pos_,  # Coarse-grained tag
                       word.tag_,  # Fine-grained tag
                       '_',
                       head_idx,  # Head of current  Index
                       word.dep_,  # Relation
                       '_', '_'])
    return tuples


def remove_noisy(content):
    """Remove brackets"""
    p1 = re.compile(r'（[^）]*）')
    p2 = re.compile(r'\([^\)]*\)')
    return p2.sub('', p1.sub('', content))


def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    return s


class NewsMining:
    """News Mining"""

    def __init__(self):
        self.textranker = textrank.TextRank()
        self.events = []
        self.result_dict = {}
        self.ners = ['PERSON', 'ORG', 'GPE']
        self.ner_dict = {
            'PERSON': 'Person',  # People, including fictional
            'ORG': 'Organization',  # Companies, agencies, institutions, etc.
            'GPE': 'Location',  # Countries, cities, states.
        }
        # dependency markers for subjects
        self.SUBJECTS = {"nsubj", "nsubjpass",
                         "csubj", "csubjpass", "agent", "expl"}
        # dependency markers for objects
        self.OBJECTS = {"dobj", "dative", "attr", "oprd"}

        self.graph_shower = graph_show.GraphShow()

    def collect_ners(self, ents):
        """Collect token only with PERSON, ORG, GPE"""
        collected_ners = []
        for token in ents:
            if token.label_ in self.ners:
                collected_ners.append(token.text + '/' + token.label_)
        return collected_ners

    def complete_VOB(self, verb, child_dict_list):
        '''Find VOB by SBV'''
        for child in child_dict_list:
            word = child[0]
            # child_dict: {'dobj': [[7, 'startup', 'NOUN', buying, 5, 'dobj']], 'prep': [[8, 'for', 'ADP', buying, 5,
            # 'prep']]}
            child_dict = child[3]
            if word == verb:
                for object_type in self.OBJECTS:  # object_type: 'dobj'
                    if object_type not in child_dict:
                        continue
                    # [7, 'startup', 'NOUN', buying, 5, 'dobj']
                    vob = child_dict[object_type][0]
                    obj = vob[1]  # 'startup'
                    return obj
        return ''

    def extract_triples(self, sent):
        svo = []
        tuples = syntax_parse(sent)
        child_dict_list = build_parse_chile_dict(sent, tuples)
        for tuple in tuples:
            rel = tuple[-1]
            if rel in self.SUBJECTS:
                sub_wd = tuple[1]
                verb_wd = tuple[3]
                obj = self.complete_VOB(verb_wd, child_dict_list)
                subj = sub_wd
                verb = verb_wd.text
                if not obj:
                    svo.append([subj, verb])
                else:
                    svo.append([subj, verb + ' ' + obj])
        return svo

    def extract_keywords(self, words_postags):
        return self.textranker.extract_keywords(words_postags, 10)

    def main(self, data_object):
        '''Main function'''
        global result_dict
        contents = []
        ids = []
        news_title = {}
        for content in data_object:
            contents.append(content[1])
        for id in data_object:
            ids.append(id[1])
        for i in data_object:
            print(i[0], i[1])
        words_postags = []  # token and its POS tag
        ner_sents = []  # store sentences which contain NER entity
        ners = []  # store all NER entity from whole article
        triples = []  # store subject verb object
        events = []  # store events
        # contents = data_object[1]
        # print(contents[0])
        # content_ids = data_object[0]
        # print(contents)
        tmp_id = {}
        for idx_count, content in enumerate(tqdm(contents)):
            # content_id = content_ids[idx]
            # 01 remove linebreaks and brackets
            try:
                content = remove_noisy(content + ".")
                content = clean_spaces(content)

                # 02 split to sentences
                doc = nlp(content)

                for i, sent in enumerate(doc.sents):
                    words_postags = [[token.text, token.pos_] for token in sent]
                    words = [token.text for token in sent]
                    postags = [token.pos_ for token in sent]
                    ents = nlp(sent.text).ents  # NER detection
                    collected_ners = self.collect_ners(ents)

                    if collected_ners:  # only extract triples when the sentence contains 'PERSON', 'ORG', 'GPE'
                        triple = self.extract_triples(sent)
                        if not triple:
                            continue
                        triples += triple
                        ners += collected_ners
                        ner_sents.append(
                            [token.text + '/' + token.label_ for token in sent.ents])

                # 03 get keywords
                keywords = [i[0] for i in self.extract_keywords(words_postags)]

                for t in triples:
                    if (t[0] in keywords or t[1] in keywords) and len(t[0]) > 1 and len(t[1]) > 1:
                        events.append([t[0], t[1]])

                # 05 get word frequency and add to events
                word_dict = [i for i in Counter([i[0] for i in words_postags if i[1] in [
                    'NOUN', 'PROPN', 'VERB'] and len(i[0]) > 1]).most_common()][:10]

                ner_dict = {i[0]: i[1] for i in Counter(ners).most_common(20)}

                for ner in ner_dict:
                    name = ner.split('/')[0]  # Jessica Miller
                    cate = self.ner_dict[ner.split('/')[1]]  # PERSON
                    events.append([name, cate])
                # print(events)
                for label_id in events:
                    if label_id[0] in tmp_id.keys():
                        continue
                    tmp_id[label_id[0]] = idx_count
                # print(events)
                # 07 get all NER entity co-occurrence information

                co_dict = collect_coexist(ner_sents, list(ner_dict.keys()))
                co_events = [[i.split('@')[0].split(
                    '/')[0], i.split('@')[1].split('/')[0]] for i in co_dict]
                events += co_events

                result_dict = {}

                for item in ner_dict:
                    parts = item.split('/')
                    if len(parts) == 2:
                        key, value = parts
                        result_dict[key] = value

            except:
                pass

        with open('test_json.json', 'r') as file:
            data = json.load(file)

        lables = [i['label'] for i in data['edges']]

        for k, i in enumerate(events):
            for j in i:
                if j in lables:
                    pass
                else:
                    try:
                        events.remove(i)
                        events_test = [sublist for l, sublist in enumerate(events) if l != k]
                    except:
                        pass

        tmp_event = []
        Ner_data = {"Person": 0, "Location": 0, "Organization": 0}
        test_data = []

        for k, i in enumerate(events):
            if i[1] == "Organization":
                Ner_data['Organization'] += 1
            if i[1] == "Location":
                Ner_data['Location'] += 1
            if i[1] == "Person":
                Ner_data['Person'] += 1

        org_count = 0
        for k, i in enumerate(events):
            tmp_dir_ner = []

            if org_count < 3:
                if i[1] == "Organization":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Person')
                    events.append(tmp_dir_ner)
                    org_count += 1
                if i[1] == "Location":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Person')
                    events.append(tmp_dir_ner)
                    org_count += 1
                if i[1] == "Person":
                    tmp_dir_ner.append(i[0])
                    tmp_dir_ner.append('Location')
                    events.append(tmp_dir_ner)
                    org_count += 1
            else:
                events = [sublist for l, sublist in enumerate(events) if l != k]

        unique_data = list({tuple(x): x for x in events}.values())
        self.graph_shower.create_page(unique_data, result_dict)
        nodes, edge = self.graph_shower.return_edge(unique_data, result_dict)
        # print(edge)
        tmp_list = [i['label'] for i in edge]
        data = {'nodes': nodes, 'edges': edge}
        g = textrank.TextrankGraph()
        nodes_rank = g.rank()

        # print(content_ids)
        # print(tmp_id)
        #========================finding the id and assinge to the labe in in nodes =========================
        for i, edge in enumerate(data['edges']):
            # nodes['id'] = content_ids[i]  
            # print(content_ids[i])
            if edge['label'] in result_dict.keys():
                edge['ner'] = result_dict[edge['label']]
            else:
                edge['ner'] = None
            if edge['label'] in tmp_id.keys():
                # print(edge['label'],tmp_id[edge['label']])
                edge['doc_id'] = tmp_id[edge['label']]
            #=========================match the list of obejct and assigne the news title to label#===============
            # for news_list in data_object:
            #     if news_list[0]==tmp_id[edge['label']]:
            #         # print(news_list[1])
            #         edge['label']=str(news_list[0])

            # print(edge['label'])
            # label_id=tmp_id[edge['label']]
            # print(edge['label'],label_id)
        # print(data['edges'])
        unique_edges = []
        seen_labels = set()
        for edge in data['edges']:
            label = (edge['label'], edge['category'], edge['ner'], edge['value'])
            if label not in seen_labels:
                unique_edges.append(edge)
                seen_labels.add(label)
        data['edges'] = unique_edges
        # nodes_rank = sorted(tmp_list, key=lambda asd: asd[1], reverse=True)

        self.events = events
        self.result_dict = result_dict

        with open('events.json', 'w') as json_file:
            json.dump(events, json_file)
        with open('result_dic.json', 'w') as json_file:
            json.dump(result_dict, json_file)
        # print(data)
        with open('graph_data.json', 'w') as json_file:
            json.dump(data, json_file)

        # for i, node in enumerate(nodes):
        #     node['distance'] = 0
        # node['id'] = content_ids[i]
        # for i, edges in enumerate(edge):
        #     edges['distance'] = 0
        # edges['id'] = content_ids[i]
        data = {'nodes': nodes, "edges": edge}
        # print(data)
        with open("query_graph.json", 'w') as file:
            json.dump(data, file)

        json_form.format_json_file('graph_data.json')
        json_form.format_json_file('query_graph.json')
        json_form.format_json_file('graph_data.json')

        # def get_events(self):
        #     return self.events, self.result_dict
