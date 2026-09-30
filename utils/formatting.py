"""Helper formatting utilities."""


def format_kes(value: float) -> str:
    """Format a number as Kenyan Shillings with thousands separators."""
    return f"KES {value:,.2f}"
