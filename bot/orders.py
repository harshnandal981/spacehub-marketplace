"""Order placement logic for Binance Futures Testnet."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)
_VALID_SIDES = {"BUY", "SELL"}


def _normalize_side(side: str) -> str:
    """Normalize and validate an order side value."""
    normalized_side = side.upper().strip()
    if normalized_side not in _VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Supported values are BUY and SELL.")
    return normalized_side


def _build_order_response(order_response: Dict[str, Any]) -> Dict[str, Any]:
    """Build a consistent, structured response from a Binance order payload."""
    executed_qty_raw = order_response.get("executedQty", "0")
    avg_price_raw: Optional[str] = order_response.get("avgPrice")

    avg_price: Optional[str] = avg_price_raw if avg_price_raw not in (None, "", "0", "0.0", "0.00000000") else None
    if avg_price is None:
        try:
            executed_qty = float(executed_qty_raw)
            cum_quote = float(order_response.get("cumQuote", "0"))
            if executed_qty > 0 and cum_quote > 0:
                avg_price = str(cum_quote / executed_qty)
        except (TypeError, ValueError):
            avg_price = None

    return {
        "orderId": order_response.get("orderId"),
        "status": order_response.get("status"),
        "executedQty": executed_qty_raw,
        "avgPrice": avg_price,
    }


def _create_futures_order(client: Any, **order_params: Any) -> Dict[str, Any]:
    """Create a futures order and return a standardized response payload."""
    logger.info("Sending futures order request: %s", order_params)
    try:
        raw_response = client.futures_create_order(**order_params)
        structured_response = _build_order_response(raw_response)
        logger.info("Futures order created successfully: %s", structured_response)
        return structured_response
    except (BinanceAPIException, BinanceRequestException) as exc:
        logger.exception("Binance API error while placing futures order.")
        raise RuntimeError(f"Binance order request failed: {exc}") from exc
    except Exception as exc:
        logger.exception("Unexpected error while placing futures order.")
        raise RuntimeError("Unexpected error while creating futures order.") from exc


def place_market_order(client: Any, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
    """Place a market futures order for a symbol and return a structured response."""
    normalized_side = _normalize_side(side)
    return _create_futures_order(
        client,
        symbol=symbol,
        side=normalized_side,
        type="MARKET",
        quantity=quantity,
    )


def place_limit_order(
    client: Any,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> Dict[str, Any]:
    """Place a limit futures order for a symbol and return a structured response."""
    normalized_side = _normalize_side(side)
    return _create_futures_order(
        client,
        symbol=symbol,
        side=normalized_side,
        type="LIMIT",
        quantity=quantity,
        price=price,
        timeInForce="GTC",
    )
