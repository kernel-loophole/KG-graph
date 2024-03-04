# News Mining

This Python module performs news mining tasks such as named entity recognition (NER), extracting triples from sentences, identifying keywords, and more.

## Dependencies
- `re`
- `collections`
- `spacy`
- `json`

## Installation
1. Clone the repository.
2. Install the required dependencies mentioned above.

## Usage
1. Instantiate the `NewsMining` class.
2. Call the `main(content)` method with the content you want to analyze.

Example:
```python
from news_mining import NewsMining

nm = NewsMining()
content = "This is a sample news article content."
nm.main(content)
events, result_dict = nm.get_events()
# Graph Processor

The Graph Processor module is designed to process graph data and perform operations such as breadth-first search (BFS) related node exploration and retrieval of labels by IDs. It is primarily used in conjunction with the News Mining module to analyze news articles and extract relevant information.

## Features

- **BFS Related Nodes**: Performs a breadth-first search on a graph structure to explore related nodes based on a provided keyword.
- **Label Retrieval by IDs**: Retrieves labels associated with node IDs from a graph structure.

## Dependencies

- `queue`: Provides a queue data structure for BFS implementation.
- `json`: Library for reading and writing JSON data.
- `graph_show`: Module for displaying graph visualizations.
- `news_graph`: Module for news mining operations.

## Usage

1. Instantiate the `GraphProcessor` class by providing the path to a JSON file containing graph data.
2. Use the `bfs_related_nodes(keyword)` method to explore related nodes based on a keyword.
3. Use the `get_labels_by_ids(node_ids)` method to retrieve labels associated with node IDs.

Example:

```python
from graph_processor import GraphProcessor

# Instantiate GraphProcessor with graph data from 'graph_data.json'
processor = GraphProcessor('graph_data.json')

# Perform BFS exploration for related nodes based on the keyword 'Elon Musk'
related_nodes = processor.bfs_related_nodes('Elon Musk')

# Retrieve labels associated with node IDs
node_ids = [1, 2, 3]  # Example node IDs
labels = processor.get_labels_by_ids(node_ids)

