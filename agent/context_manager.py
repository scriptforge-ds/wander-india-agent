MAX_MESSAGES = 20

def build_context(messages: list) -> list:
    trimmed = messages[-MAX_MESSAGES:]

    formatted = []
    for msg in trimmed:
        role = "model" if msg["role"] == "assistant" else "user"
        formatted.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    return formatted


def add_message(messages: list, role: str, content: str) -> list:
    messages.append({"role": role, "content": content})
    return messages