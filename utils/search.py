def search(record):
    parts = []

    for attr in dir(record):
        if attr.startswith("_"):
            continue

        value = getattr(record, attr, None)
        if not value:
            continue

        try:
            if attr == "phones" or attr == "emails":
                parts.append(" ".join(p.value for p in value))
            else:
                parts.append(value.value)
        except AttributeError:
            continue

    return " ".join(parts).lower()
