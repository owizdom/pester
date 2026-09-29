"""Sentence-level lexicon matching against analysis/lexicon.txt."""
import re
from pathlib import Path


def _load():
    sections, cur = {}, None
    for line in (Path(__file__).parent / "lexicon.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            cur = sections.setdefault(line.strip("[]"), [])
        else:
            cur.append(line.lower())
    return sections


LEX = _load()


def _has(sentence, terms):
    return any(re.search(r"\b" + re.escape(t) + r"\b", sentence) for t in terms)


def _sentences(text):
    return [s.lower() for s in re.split(r"(?<=[.!?;])\s+|\n+", text) if s.strip()]


def is_ack(text):
    return any(_has(s, LEX["reference"]) for s in _sentences(text))


def is_irritated(text):
    return any(_has(s, LEX["reference"]) and _has(s, LEX["irritation"]) for s in _sentences(text))
