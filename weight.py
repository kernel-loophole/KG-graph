from collections import Counter
import re

def calculate_keyword_importance(documents):
    combined_text = ' '.join(documents)
    tokens = re.findall(r'\b\w+\b', combined_text.lower())
    word_freq = Counter(tokens)
    total_words = sum(word_freq.values())
    normalized_freq = {word: freq / total_words for word, freq in word_freq.items()}
    
    return normalized_freq

documents = [
    "This is a sample document.",
    "Another sample document with repeated words."
]

keyword_importance = calculate_keyword_importance(documents)

for word, importance in sorted(keyword_importance.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {importance}")
