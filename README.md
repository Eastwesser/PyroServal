# Pyrogram Bot

A simple Pyrogram bot template with SQLAlchemy integration for handling messages and user statuses.

## Features

- Handles incoming messages from users
- Updates user statuses based on keywords present in the messages
- Uses Pyrogram for Telegram bot API interactions
- Utilizes SQLAlchemy for database management

## Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.10
- Pyrogram
- SQLAlchemy
- asyncpg (for PostgreSQL async database)
- tgcrypto (for improved Pyrogram performance)

You'll also need to create a PostgreSQL database and set up environment variables for API credentials and database
connection URL.

## Installation

1. Clone the repository:

git clone https://github.com/Eastwesser/PyroBot.git

2. Install the dependencies:

pip install -r requirements.txt

3. Set up environment variables:

Create a `.env` file in the project root directory and add the following variables:

- API_ID=your_api_id
- API_HASH=your_api_hash
- BOT_TOKEN=your_bot_token
- DB_URL=postgresql://username@localhost/mydatabase

Replace `your_api_id`, `your_api_hash`, `your_bot_token`, `username`, `password`, and `mydatabase` with your actual
values.

4. Run the bot:

python main.py

## Usage

- Start the bot and interact with it in your Telegram chat. Use keywords like "прекрасно" or "ожидать" to trigger status
  updates for users.
- Customize the bot logic in `main.py` according to your requirements.

## Acknowledgements

- [Pyrogram](https://github.com/pyrogram/pyrogram) - Telegram bot framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping (ORM) library
- [asyncpg](https://pypi.org/project/asyncpg/) - Async PostgreSQL adapter for Python
- [tgcrypto](https://pypi.org/project/tgcrypto/) - Cryptographic backend for Pyrogram

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
