def format_report(inv):
    lines = []
    for sku in sorted(inv.skus()):
        lines.append(f"{sku}: {inv.qty(sku)}")
    lines.append(f"TOTAL: {inv.total_value():.2f}")
    return "\n".join(lines)
