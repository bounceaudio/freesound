"""
Basic smoke tests for the freesound-python package.

These tests verify that the package can be imported and basic
functionality works without requiring API keys.
"""
import unittest
from unittest.mock import Mock, patch
import freesound


class TestFreesoundImport(unittest.TestCase):
    """Test that the module can be imported and basic classes exist."""

    def test_module_import(self):
        """Test that the freesound module can be imported."""
        self.assertIsNotNone(freesound)

    def test_client_class_exists(self):
        """Test that FreesoundClient class exists."""
        self.assertTrue(hasattr(freesound, 'FreesoundClient'))

    def test_client_instantiation(self):
        """Test that FreesoundClient can be instantiated."""
        client = freesound.FreesoundClient()
        self.assertIsNotNone(client)
        self.assertIsNone(client.auth)

    def test_set_token(self):
        """Test that set_token method works."""
        client = freesound.FreesoundClient()
        client.set_token("test_token")
        self.assertIsNotNone(client.auth)

    def test_set_token_oauth(self):
        """Test that set_token works with OAuth type."""
        client = freesound.FreesoundClient()
        client.set_token("test_oauth_token", "oauth")
        self.assertIsNotNone(client.auth)


class TestFreesoundURIS(unittest.TestCase):
    """Test the URIS class."""

    def test_uris_class_exists(self):
        """Test that URIS class exists."""
        self.assertTrue(hasattr(freesound, 'URIS'))

    def test_base_uri(self):
        """Test that base URI is correct."""
        self.assertEqual(freesound.URIS.BASE, 'https://freesound.org/apiv2')

    def test_uri_generation(self):
        """Test URI generation with parameters."""
        uri = freesound.URIS.uri(freesound.URIS.SOUND, 12345)
        self.assertEqual(uri, 'https://freesound.org/apiv2/sounds/12345/')


class TestFreesoundAuth(unittest.TestCase):
    """Test authentication classes."""

    def test_token_auth_class_exists(self):
        """Test that FreesoundTokenAuth class exists."""
        self.assertTrue(hasattr(freesound, 'FreesoundTokenAuth'))

    def test_token_auth_token_type(self):
        """Test token authentication with token type."""
        auth = freesound.FreesoundTokenAuth("test_token", "token")
        self.assertEqual(auth.header, "Token test_token")

    def test_token_auth_oauth_type(self):
        """Test token authentication with OAuth type."""
        auth = freesound.FreesoundTokenAuth("test_token", "oauth")
        self.assertEqual(auth.header, "Bearer test_token")

    def test_token_auth_callable(self):
        """Test that auth object can be called on a request."""
        auth = freesound.FreesoundTokenAuth("test_token")
        mock_request = Mock()
        mock_request.headers = {}
        result = auth(mock_request)
        self.assertEqual(mock_request.headers['Authorization'], "Token test_token")


if __name__ == '__main__':
    unittest.main()
