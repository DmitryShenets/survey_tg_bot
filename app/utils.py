async def replace_key_value(data: dict) -> dict:
    return {v: k for k, v in data.items()}
