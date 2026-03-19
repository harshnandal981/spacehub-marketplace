"""CLI entry point placeholders for the trading bot."""

from __future__ import annotations

import argparse
import logging
from typing import Any, Dict

from bot.client import BinanceClient
from bot.logging_config import log_api_error, log_api_request, log_api_response, setup_logging
from bot.orders import place_limit_order, place_market_order
from bot.validators import validate_order_inputs

logger = logging.getLogger(__name__)


def _normalize_text(value: str) -> str:
    """Normalize text-based CLI inputs to uppercase without surrounding spaces."""
    return value.strip().upper()


def _print_order_summary(args: argparse.Namespace) -> None:
    """Print a readable summary of the order request from parsed CLI arguments."""
    print("Order Summary")
    print("-------------")
    print(f"Symbol:   {args.symbol}")
    print(f"Side:     {args.side}")
    print(f"Type:     {args.order_type}")
    print(f"Quantity: {args.quantity}")
    if args.order_type == "LIMIT":
        print(f"Price:    {args.price}")


def _print_response_details(response: Dict[str, Any]) -> None:
    """Print a readable summary of important order response fields."""
    print("\nResponse Details")
    print("----------------")
    print(f"Order ID:     {response.get('orderId')}")
    print(f"Status:       {response.get('status')}")
    print(f"Executed Qty: {response.get('executedQty')}")
    print(f"Avg Price:    {response.get('avgPrice')}")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet orders from the command line.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading symbol, for example BTCUSDT.",
    )
    parser.add_argument(
        "--side",
        required=True,
        type=_normalize_text,
        help="Order side: BUY or SELL.",
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        type=_normalize_text,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT.",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity as a positive number.",
    )
    parser.add_argument(
        "--price",
        type=float,
        help="Limit price. Required when --type LIMIT is used.",
    )
    return parser


def run_cli(args: argparse.Namespace) -> int:
    """Execute CLI flow based on parsed arguments."""
    setup_logging()

    try:
        validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        _print_order_summary(args)
        binance_client = BinanceClient().get_client()

        request_payload: Dict[str, Any] = {
            "symbol": args.symbol,
            "side": args.side,
            "type": args.order_type,
            "quantity": args.quantity,
        }
        if args.order_type == "LIMIT":
            request_payload["price"] = args.price

        log_api_request("futures_create_order", request_payload)
        if args.order_type == "MARKET":
            response = place_market_order(
                client=binance_client,
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
            )
        else:
            response = place_limit_order(
                client=binance_client,
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
            )
        log_api_response("futures_create_order", response)

        _print_response_details(response)
        print("\nSuccess: order placed successfully.")
        return 0
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"Validation error: {exc}")
        print("Failure: order was not submitted.")
        return 2
    except (RuntimeError, ConnectionError, PermissionError) as exc:
        logger.error("API/client error: %s", exc)
        log_api_error("futures_create_order", exc)
        print(f"API error: {exc}")
        print("Failure: order request failed.")
        return 1
    except Exception as exc:
        logger.exception("Unexpected error while running CLI.")
        log_api_error("cli_run", exc)
        print(f"Unexpected error: {exc}")
        print("Failure: unexpected exception occurred.")
        return 1


def main() -> int:
    """Parse arguments and execute the CLI application."""
    parser = build_parser()
    args = parser.parse_args()
    return run_cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
