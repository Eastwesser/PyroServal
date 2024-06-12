import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.database.models.models import User
from app.handlers.message_handlers import register_handlers


class TestTriggerWords(unittest.TestCase):

    @patch('app.database.database.get_db')
    async def test_check_for_trigger_words(self, mock_get_db):
        mock_message = MagicMock()
        mock_message.from_user.id = 123
        mock_message.text = "Прекрасно"
        mock_message.reply = AsyncMock()

        mock_db = MagicMock()
        mock_get_db.return_value.__aenter__.return_value = mock_db

        mock_user = User(id=123, message_text="some text")
        mock_db.execute.return_value.scalars.return_value.first.return_value = mock_user

        mock_client = MagicMock()

        await register_handlers(mock_client, mock_message)

        mock_message.reply.assert_called_once_with("Ваша воронка успешно завершена!")


if __name__ == "__main__":
    unittest.main()
