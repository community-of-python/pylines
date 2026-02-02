def parse_value(value_text: str) -> int | None:
    try:
        return int(value_text)
    except Exception:
        return None
