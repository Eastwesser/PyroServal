import unittest
from unittest.mock import AsyncMock, MagicMock

from pyrogram import Client, types

from app.handlers.message_handlers import handle_message  # Update with actual import path


class TestMessageHandlers(unittest.IsolatedAsyncioTestCase):

    async def test_handle_message(self):
        mock_message = MagicMock(spec=types.Message)
        mock_message.configure_mock(from_user=MagicMock(id=123))
        mock_message.text = "Прекрасно"
        mock_message.reply = AsyncMock()

        # Mock the client and its on_message method
        mock_client = MagicMock(spec=Client)
        mock_client.on_message = AsyncMock()

        # Assuming handle_message is the function that processes the message
        await handle_message(mock_client, mock_message)

        # Check if the reply method was called
        mock_message.reply.assert_called()


if __name__ == '__main__':
    unittest.main()
