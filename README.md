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

