def search(record):
    parts = []

    for attr in dir(record):
        if attr.startswith("_"):
            continue

        value = getattr(record, attr, None)
        if not value:
            continue

        try:
            if attr in ("phones", "emails"):
                parts.append(" ".join(str(p.value) for p in value))
            else:
                val = value.value
                if isinstance(val, (list, tuple)):
                    parts.append(" ".join(str(v) for v in val))
                else:
                    parts.append(str(val))
        except AttributeError:
            continue

    return " ".join(parts).lower()
