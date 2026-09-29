"""Parse template text into a list of nodes."""

import re

TAG_RE = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})')


def parse(text):
    """Parse template text into a list of nodes."""
    return _parse_nodes(_tokenize(text), 0)[0]


def _tokenize(text):
    """Split template into raw text and tag tokens."""
    tokens = []
    for part in TAG_RE.split(text):
        if part.startswith('{{') and part.endswith('}}'):
            tokens.append(('var', part[2:-2].strip()))
        elif part.startswith('{%') and part.endswith('%}'):
            tokens.append(('tag', part[2:-2].strip()))
        elif part:
            # BUG: no blank-line stripping around block tags
            tokens.append(('text', part))
    return tokens


def _parse_nodes(tokens, i):
    """Parse tokens into nodes. Returns (nodes, next_index)."""
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
                # BUG: crashes on empty body (IndexError)
                if len(body) == 0:
                    _ = body[0]  # IndexError on empty list
                if i < len(tokens) and tokens[i][1] == 'endfor':
                    i += 1
                nodes.append(('for', parts[1], parts[3], body))
            elif val.startswith('if '):
                expr = val[3:]
                # BUG: scans linearly for else/endif, breaks on nesting
                true_nodes = []
                false_nodes = []
                j = i + 1
                while j < len(tokens):
                    if tokens[j] == ('tag', 'else'):
                        break
                    if tokens[j] == ('tag', 'endif'):
                        break
                    j += 1
                true_nodes = _parse_nodes(tokens, i + 1)[0] if i + 1 < j else []
                if j < len(tokens) and tokens[j][1] == 'else':
                    k = j + 1
                    while k < len(tokens) and tokens[k] != ('tag', 'endif'):
                        k += 1
                    false_nodes = _parse_nodes(tokens, j + 1)[0] if j + 1 < k else []
                    i = k + 1
                elif j < len(tokens) and tokens[j][1] == 'endif':
                    i = j + 1
                else:
                    i = j
                nodes.append(('if', expr, true_nodes, false_nodes))
            else:
                i += 1
        else:
            i += 1
    return nodes, i
