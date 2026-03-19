"""Input validation placeholders for trading operations."""

from __future__ import annotations

from typing import Any, Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def _to_positive_float(value: Any, field_name: str) -> float:
    """Convert a value to a positive float for a numeric input field."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc

    if numeric_value <= 0:
        raise ValueError(f"{field_name} must be a positive number.")
    return numeric_value


def validate_symbol(symbol: str) -> bool:
    """Validate that symbol is a non-empty string."""
    if not isinstance(symbol, str):
        raise ValueError("symbol must be a string.")
    if not symbol.strip():
        raise ValueError("symbol cannot be empty.")
    return True


def validate_side(side: str) -> bool:
    """Validate that side is either BUY or SELL."""
    if not isinstance(side, str):
        raise ValueError("side must be a string.")

    normalized_side = side.strip().upper()
    if normalized_side not in VALID_SIDES:
        raise ValueError("side must be either BUY or SELL.")
    return True


def validate_order_type(order_type: str) -> bool:
    """Validate that order type is either MARKET or LIMIT."""
    if not isinstance(order_type, str):
        raise ValueError("order type must be a string.")

    normalized_order_type = order_type.strip().upper()
    if normalized_order_type not in VALID_ORDER_TYPES:
        raise ValueError("order type must be either MARKET or LIMIT.")
    return True


def validate_quantity(quantity: float) -> bool:
    """Validate that quantity is a positive float."""
    _to_positive_float(quantity, "quantity")
    return True


def validate_price(price: Optional[float], order_type: str) -> bool:
    """Validate that price is provided and positive for LIMIT orders."""
    validate_order_type(order_type)

    normalized_order_type = order_type.strip().upper()
    if normalized_order_type == "LIMIT":
        if price is None:
            raise ValueError("price is required for LIMIT orders.")
        _to_positive_float(price, "price")
    return True


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> bool:
    """Validate all common order inputs for CLI commands."""
    validate_symbol(symbol)
    validate_side(side)
    validate_order_type(order_type)
    validate_quantity(quantity)
    validate_price(price, order_type)
    return True
