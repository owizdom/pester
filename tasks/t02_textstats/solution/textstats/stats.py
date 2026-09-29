from collections import Counter

from textstats.tokenize import sentences, words


def word_freq(text):
    return Counter(words(text))


def top_n(text, n):
    items = sorted(word_freq(text).items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in items[:n]]


def average_word_length(text):
    ws = words(text)
    return sum(len(w) for w in ws) / len(ws) if ws else 0.0


def average_sentence_length(text):
    ss = sentences(text)
    return sum(len(words(s)) for s in ss) / len(ss) if ss else 0.0
