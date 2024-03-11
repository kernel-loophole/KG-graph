# News Graph

Key information extration from text and graph visilization. Inspired by [TextGrapher](https://github.com/liuhuanyong/TextGrapher).

# Project Introduction

<<<<<<< HEAD
How to represent a text in a simple way is a chanllenge topic. This peoject try to extraction key information from the text by NLP methods, which contain NER extraction, relation detection, keywords extraction, frequencies words extraction. And finally show the key information in a graph way.

# How to use
=======
# Graph 
open HTML file to view graph.after running main.py file.
# Installation
1. Clone the repository.
2. Install the required dependencies mentioned above.

# Usage
1. Instantiate the `NewsMining` class.
2. Call the `main(content)` method with the content you want to analyze.

Example:
```python
from news_mining import NewsMining

nm = NewsMining()
content = "This is a sample news article content."
nm.main(content)
events, result_dict = nm.get_events()
```
![Graph Processor](grap.png)
# Graph Processor

The Graph Processor module is designed to process graph data and perform operations such as breadth-first search (BFS) related node exploration and retrieval of labels by IDs. It is primarily used in conjunction with the News Mining module to analyze news articles and extract relevant information.

# Features

- **BFS Related Nodes**: Performs a breadth-first search on a graph structure to explore related nodes based on a provided keyword.
- **Label Retrieval by IDs**: Retrieves labels associated with node IDs from a graph structure.

# Dependencies

- `queue`: Provides a queue data structure for BFS implementation.
- `json`: Library for reading and writing JSON data.
- `graph_show`: Module for displaying graph visualizations.
- `news_graph`: Module for news mining operations.

# Usage

1. Instantiate the `GraphProcessor` class by providing the path to a JSON file containing graph data.
2. Use the `bfs_related_nodes(keyword)` method to explore related nodes based on a keyword.
3. Use the `get_labels_by_ids(node_ids)` method to retrieve labels associated with node IDs.

Example:
>>>>>>> f9d64f6e1c0e3e9d04ec10abceb7f947d747c40f

```python
from news_graph import NewsMining
content = 'Input you text here'
Miner = NewsMining()
Miner.main(content)
```

This will generate the `graph.html`. 

# Example Demo

1) [Blockbuster *The Wandering Earth*](https://www.theverge.com/2019/2/9/18218479/the-wandering-earth-review-film-china-first-science-fiction-blockbuster-cixin-liu-gravity-the-core)
![image1](https://ws4.sinaimg.cn/large/006tNc79gy1g02ikc4mqjj30n60ot42a.jpg)

2) [Tokyo Marathon 2019 Elite Field](https://www.marathon.tokyo/en/news/detail/news_001178.html)
![image](https://user-images.githubusercontent.com/10768193/83982855-d4c93000-a964-11ea-86d8-1dd19f7d5334.png)
)

3) [EVEN ANONYMOUS CODERS LEAVE FINGERPRINTS](https://www.wired.com/story/machine-learning-identify-anonymous-code/?utm_campaign=Deep%20Learning%20Weekly&utm_medium=email&utm_source=Revue%20newsletter)
![image3](https://ws3.sinaimg.cn/large/006tNc79gy1g02hulrjx8j30i00pvjuv.jpg)
