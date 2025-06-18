def summarize_text(text: str) -> str:
    """Return a simple truncated summary."""
    trimmed = text.strip()
    summary = trimmed[:100]
    if len(trimmed) > 100:
        summary += "..."
    return summary