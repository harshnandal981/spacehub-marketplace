"""Binance Futures Testnet client wrapper."""

from __future__ import annotations

import logging
import os
from typing import Any, List

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class BinanceClient:
    """Wrapper class for initializing and exposing a Binance Futures Testnet client."""

    def __init__(self) -> None:
        """Initialize the Binance client using API credentials from environment variables."""
        load_dotenv()

        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")
        if not api_key or not api_secret:
            logger.error("Missing API credentials in .env. Expected API_KEY and API_SECRET.")
            raise ValueError("Missing API credentials: API_KEY and API_SECRET are required.")

        try:
            self._client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
            self._client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            self._client.futures_ping()
            self._client.futures_account_balance()
            logger.info("Binance Futures Testnet client initialized successfully.")
        except BinanceAPIException as exc:
            if exc.code in (-2014, -2015) or exc.status_code in (401, 403):
                logger.exception("Invalid Binance API credentials for Futures Testnet.")
                raise PermissionError("Invalid API_KEY or API_SECRET for Binance Futures Testnet.") from exc

            logger.exception("Binance API error while initializing Futures Testnet client.")
            raise ConnectionError(f"Binance API error during client initialization: {exc}") from exc
        except BinanceRequestException as exc:
            logger.exception("Network error while connecting to Binance Futures Testnet.")
            raise ConnectionError("Network error while connecting to Binance Futures Testnet.") from exc
        except Exception as exc:
            logger.exception("Unexpected error while initializing Binance client.")
            raise ConnectionError("Unexpected error during Binance client initialization.") from exc

    def get_client(self) -> Client:
        """Return the initialized python-binance client instance."""
        return self._client

    def test_futures_connection(self) -> List[Any]:
        """Test Futures Testnet connectivity by fetching account balance."""
        try:
            balances = self._client.futures_account_balance()
            logger.info("Futures Testnet connection test successful.")
            return balances
        except BinanceAPIException as exc:
            if exc.code in (-2014, -2015) or exc.status_code in (401, 403):
                logger.exception("Invalid Binance API credentials during connection test.")
                raise PermissionError("Invalid API credentials while testing Futures connection.") from exc

            logger.exception("Binance API error during Futures connection test.")
            raise ConnectionError(f"Binance API error during connection test: {exc}") from exc
        except BinanceRequestException as exc:
            logger.exception("Network error during Futures connection test.")
            raise ConnectionError("Network error while testing Binance Futures connection.") from exc
        except Exception as exc:
            logger.exception("Unexpected error during Futures connection test.")
            raise ConnectionError("Unexpected error while testing Binance Futures connection.") from exc
