# News Graph

Key information extration from text and graph visilization. Inspired by [TextGrapher](https://github.com/liuhuanyong/TextGrapher).

# Project Introduction

How to represent a text in a simple way is a chanllenge topic. This peoject try to extraction key information from the text by NLP methods, which contain NER extraction, relation detection, keywords extraction, frequencies words extraction. And finally show the key information in a graph way.

# How to use
Utilizes spaCy to extract named entities such as persons, organizations, and locations from news articles.
<mark>Relationship Extraction</mark>: Identifies relationships between entities using pretrained model and generates JSON files representing node-edge relationships.
- each model and NER code genrate seprate json files 
- then we find the differnce between two json files and genrate a final json file.
- This json file will be used for BFS seacrhing and ploting of graph
- This Final json file have the ner TAG,NODE LABEL,and relationship between nodes.
```python
from news_graph import NewsMining
content = 'Input you text here'
Miner = NewsMining()
Miner.main(content)
```
This will generate the `graph.html`. 
# Overview of model and NER extraction
1) ![flow](flow.png)

# Example Demo

1) ![image1](image_03.jpg)

1) ![image1](image_05.jpg)

2) 
![image02](grap02.png)
# Node coloring
- Red:Location<br>
- Blue:Person<br>
- Green:organization<br>  
- Grey:other
<!-- 
2) [Tokyo Marathon 2019 Elite Field](https://www.marathon.tokyo/en/news/detail/news_001178.html)
![image](https://user-images.githubusercontent.com/10768193/83982855-d4c93000-a964-11ea-86d8-1dd19f7d5334.png)
)

3) [EVEN ANONYMOUS CODERS LEAVE FINGERPRINTS](https://www.wired.com/story/machine-learning-identify-anonymous-code/?utm_campaign=Deep%20Learning%20Weekly&utm_medium=email&utm_source=Revue%20newsletter)
![image3](https://ws3.sinaimg.cn/large/006tNc79gy1g02hulrjx8j30i00pvjuv.jpg) -->
# Loading the SpaCy Model
The following line initializes the SpaCy language model for English language processing:
```python
nlp = spacy.load('en_core_web_lg')
```
The model loaded here is 'en_core_web_lg', which is a large English language model trained on web text data.

# Defining the NewsMining Class
The code defines a Python class named NewsMining, encapsulating functionality related to news mining:
Initializing the NewsMining Class
The constructor method (__init__) initializes various attributes of the NewsMining class:


# Additional Methods
The code snippet also includes additional methods such as clean_spaces, remove_noisy, and collect_ners, which perform tasks like cleaning text, removing noisy characters, and collecting named entities, respectively.

Explanation of Python Code for News Mining
Extracting Triples
The extract_triples method takes a sentence as input and returns Subject-Verb-Object (SVO) triples:
```python
def extract_triples(self, sent):
    svo = []
    tuples = self.syntax_parse(sent)
    child_dict_list = self.build_parse_chile_dict(sent, tuples)
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
```
# Extracting Keywords
The extract_keywords method extracts the top 10 keywords from a list of word-postag pairs:
```python 
def extract_keywords(self, words_postags):
        return self.textranker.extract_keywords(words_postags, 10)
```
# Main Method for News Mining
The main method is a placeholder for the main functionality of news mining:

# Getting Extracted Events and NER Results
The get_events method returns the extracted events and Named Entity Recognition (NER) results:
```python
def get_events(self):
        return self.events, self.result_dict
```
Instantiating the NewsMining Class
The NewsMining class is instantiated as news_miner:
# Call the class object
```python
news_miner = NewsMining()
```
