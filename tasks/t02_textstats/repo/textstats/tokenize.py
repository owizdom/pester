import re


def words(text):
    return re.findall(r"[A-Za-z]+", text)


def sentences(text):
    return re.split(r"\.", text)
