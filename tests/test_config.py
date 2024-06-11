# tests/test_config.py
import os
from unittest import TestCase
from unittest.mock import patch


class TestConfig(TestCase):

    @patch.dict(os.environ, {
        'API_ID': '123456',
        'API_HASH': 'fake_hash',
        'BOT_TOKEN': 'fake_token',
        'DB_URL': 'postgresql://fake:fake@localhost/fake_db'
    })
    def test_env_variables(self):
        # Remove config module from sys.modules to force reload
        import sys
        if 'app.config' in sys.modules:
            del sys.modules['app.config']

        from app.config import API_ID, API_HASH, BOT_TOKEN, DB_URL
        self.assertEqual(API_ID, '123456')
        self.assertEqual(API_HASH, 'fake_hash')
        self.assertEqual(BOT_TOKEN, 'fake_token')
        self.assertEqual(DB_URL, 'postgresql://fake:fake@localhost/fake_db')
