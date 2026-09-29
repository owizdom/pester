"""Render parsed template nodes with a context dict."""


def render(nodes, context):
    """Render a list of parsed nodes to a string.
    BUG: no HTML escaping on variable output.
    BUG: KeyError on undefined variables.
    BUG: for-loop crashes on empty lists."""
    output = []
    for node in nodes:
        if node[0] == 'text':
            output.append(node[1])

        elif node[0] == 'var':
            name = node[1]
            # BUG: no HTML escaping, crashes on missing keys
            output.append(str(context[name]))

        elif node[0] == 'for':
            _, var_name, list_name, body = node
            items = context[list_name]
            # BUG: crashes on empty list because body rendering
            # tries to access items[0] for type checking
            if len(items) == 0:
                # attempt to check first item type
                first = items[0]  # IndexError!
            for item in items:
                child_ctx = dict(context)
                child_ctx[var_name] = item
                output.append(render(body, child_ctx))

        elif node[0] == 'if':
            _, expr, true_nodes, false_nodes = node
            val = context.get(expr.strip())
            if val:
                output.append(render(true_nodes, context))
            else:
                output.append(render(false_nodes, context))

    return ''.join(output)
