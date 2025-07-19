def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def record_to_dict(record):
    fields = ["promid", "name", "phones", "emails", "birthday", "address"]
    return {
        field: (
            ", ".join(phone.value for phone in getattr(record, field, []))
            if field in ("phones", "emails")
            else getattr(getattr(record, field, None), "value", "-")[0]
            if field == "promid"
            else getattr(getattr(record, field, None), "value", "-")
        )
        for field in fields
    }


def notes_to_dict(record):
    fields = ["title", "description"]
    return {
        field: (
            getattr(getattr(record, field, None), "value", "-")[0]
            if field == "promid"
            else getattr(getattr(record, field, None), "value", "-")
        )
        for field in fields
    }