def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def record_to_dict(record):
    fields = ["name", "phones", "email", "birthday", "address"]
    return {
        field: (
            ", ".join(phone.value for phone in getattr(record, field, []))
            if field == "phones"
            else getattr(getattr(record, field, None), "value", "-")
        )
        for field in fields
    }


def notes_to_dict(record):
    fields = ["title", "description"]
    return {
        field: (
            getattr(getattr(record, field, None), "value", "-")
        )
        for field in fields
    }