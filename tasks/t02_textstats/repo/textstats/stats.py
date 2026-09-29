from collections import Counter

from textstats.tokenize import words


def word_freq(text):
    return Counter(words(text))


def top_n(text, n):
    return [w for w, _ in word_freq(text).most_common(n)]


def average_word_length(text):
    ws = words(text)
    return sum(len(w) for w in ws) / len(ws)
