import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def download_text(url):
    """Завантаження тексту з URL"""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def tokenize(text):
    """Токенізація тексту"""
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def count_words(words):
    """Підрахунок слів у тексті"""
    return Counter(words)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізація топ слів"""
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()

def map_reduce(text, num_workers=4):
    """Аналіз частоти слів за допомогою парадигми MapReduce"""
    words = tokenize(text)
    chunk_size = len(words) // num_workers

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        results = executor.map(count_words, chunks)

    total_counts = Counter()
    for result in results:
        total_counts.update(result)

    return total_counts

def main():
    url = 'https://www.gutenberg.org/files/1342/1342-0.txt'  # приклад URL
    text = download_text(url)
    word_counts = map_reduce(text)
    visualize_top_words(word_counts)

if __name__ == "__main__":
    main()
