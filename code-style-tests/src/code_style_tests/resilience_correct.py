import stamina

@stamina.retry(on=(RuntimeError,))
def fetch_data() -> str:
    return "value"
