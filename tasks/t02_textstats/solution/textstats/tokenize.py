import re


def words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower())


def sentences(text):
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
