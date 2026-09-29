def format_report(inv):
    lines = []
    for sku in sorted(inv.skus(), reverse=True):
        lines.append(f"{sku}: {inv.qty(sku)}")
    lines.append(f"TOTAL: {inv.total_value()}")
    return "\n".join(lines)
