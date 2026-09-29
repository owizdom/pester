"""Render parsed template nodes with a context dict."""

from template.filters import apply_filter


def _html_escape(s):
    """Escape HTML special characters."""
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    return s


def _resolve_var(expr, context):
    """Resolve a variable expression, possibly with filters.
    Supports: name | filter and name | filter:"arg"."""
    parts = expr.split('|')
    name = parts[0].strip()
    value = context.get(name, '')

    for filt in parts[1:]:
        filt = filt.strip()
        if ':' in filt:
            fname, farg = filt.split(':', 1)
            farg = farg.strip().strip('"').strip("'")
            value = apply_filter(value, fname.strip(), farg)
        else:
            value = apply_filter(value, filt)

    return value


def render(nodes, context):
    """Render a list of parsed nodes to a string."""
    output = []
    for node in nodes:
        if node[0] == 'text':
            output.append(node[1])

        elif node[0] == 'var':
            expr = node[1]
            value = _resolve_var(expr, context)
            output.append(_html_escape(str(value)))

        elif node[0] == 'for':
            _, var_name, list_name, body = node
            items = context.get(list_name, [])
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
