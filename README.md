# Binance Futures Testnet Trading Bot

Professional, modular Python CLI bot for placing Binance Futures Testnet orders. This project is designed for clean architecture, interview discussions, and easy extension into a production-grade bot.

## Description

This bot uses the python-binance SDK to connect to Binance Futures Testnet and place MARKET or LIMIT orders from the command line.

It includes:
- Environment-based API key management using a .env file
- Input validation for all trading arguments
- Structured order responses
- File-based logging for requests, responses, and errors

## Features

- Modular codebase with clear separation of concerns
- Binance Futures Testnet client wrapper
- Reusable order placement functions
- Reusable validators for symbol, side, order type, quantity, and price
- CLI workflow with friendly success and error output
- Centralized logging to logs/app.log

## Setup

### 1. Prerequisites

- Python 3.x
- pip

### 2. Install dependencies

~~~bash
pip install python-binance python-dotenv
~~~

### 3. Configure environment variables

Create a file named .env in the project root with the following values:

~~~env
API_KEY=your_binance_testnet_api_key
API_SECRET=your_binance_testnet_api_secret
~~~

### 4. Run commands

Use the CLI entry point at the project root:

~~~bash
python cli.py --help
~~~

## Example Commands

### MARKET order

~~~bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
~~~

### LIMIT order

~~~bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
~~~

## Project Structure

~~~text
.
├── bot/
│   ├── client.py          # Binance client wrapper for Futures Testnet
│   ├── orders.py          # Market and limit order functions
│   ├── validators.py      # Reusable CLI input validations
│   └── logging_config.py  # Logging setup and API log helpers
├── cli.py                 # CLI entry point and execution flow
└── README.md
~~~

## Assumptions

- API keys are for Binance Futures Testnet, not mainnet.
- .env is present in the project root before running commands.
- Network access to Binance Testnet is available.
- Quantity and price precision constraints are handled by Binance exchange rules and may require symbol-specific formatting in future enhancements.
- Current scope focuses on placing orders and clear CLI behavior; advanced risk management and strategy logic are out of scope.
