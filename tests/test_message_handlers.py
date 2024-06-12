import unittest
from unittest.mock import AsyncMock, MagicMock

from pyrogram import Client

from app.handlers.message_handlers import handle_message


class TestMessageHandlers(unittest.TestCase):

    async def test_handle_message(self):
        mock_message = MagicMock()
        mock_message.from_user.id = 123
        mock_message.text = "Прекрасно"
        mock_message.reply = AsyncMock()

        mock_client = MagicMock(spec=Client)

        await handle_message(mock_client, mock_message)

        mock_message.reply.assert_called()


if __name__ == "__main__":
    unittest.main()
