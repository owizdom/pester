"""Parse template text into a list of nodes."""

import re

TAG_RE = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})')


def parse(text):
    """Parse template text into a list of nodes."""
    return _parse_nodes(_tokenize(text), 0)[0]


def _tokenize(text):
    """Split template into raw text and tag tokens."""
    tokens = []
    raw = TAG_RE.split(text)
    for idx, part in enumerate(raw):
        if part.startswith('{{') and part.endswith('}}'):
            tokens.append(('var', part[2:-2].strip()))
        elif part.startswith('{%') and part.endswith('%}'):
            tokens.append(('tag', part[2:-2].strip()))
        elif part:
            val = part
            # Strip trailing whitespace before a tag
            if idx + 1 < len(raw):
                nxt = raw[idx + 1]
                if nxt.startswith('{%'):
                    val = val.rstrip(' \t')
                    if val.endswith('\n'):
                        pass
                    elif val == '':
                        continue
            # Strip leading newline after a tag
            if idx > 0:
                prev = raw[idx - 1]
                if prev.startswith('{%') and val and val[0] == '\n':
                    val = val[1:]
            if val:
                tokens.append(('text', val))
    return tokens


def _parse_nodes(tokens, i):
    """Parse tokens into nodes with proper nesting."""
    nodes = []
    while i < len(tokens):
        kind, val = tokens[i]
        if kind == 'text':
            nodes.append(('text', val))
            i += 1
        elif kind == 'var':
            nodes.append(('var', val))
            i += 1
        elif kind == 'tag':
            if val in ('else', 'endif', 'endfor'):
                return nodes, i
            if val.startswith('for '):
                parts = val.split()
                body, i = _parse_nodes(tokens, i + 1)
                if i < len(tokens) and tokens[i][1] == 'endfor':
                    i += 1
                nodes.append(('for', parts[1], parts[3], body))
            elif val.startswith('if '):
                expr = val[3:]
                true_nodes, i = _parse_nodes(tokens, i + 1)
                false_nodes = []
                if i < len(tokens) and tokens[i][1] == 'else':
                    false_nodes, i = _parse_nodes(tokens, i + 1)
                if i < len(tokens) and tokens[i][1] == 'endif':
                    i += 1
                nodes.append(('if', expr, true_nodes, false_nodes))
            else:
                i += 1
        else:
            i += 1
    return nodes, i
