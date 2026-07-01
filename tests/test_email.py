import unittest
from unittest.mock import patch, MagicMock
import smtplib

from email_sender import send_email, send_failure_notify

class TestEmailSender(unittest.TestCase):

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_success(self, mock_smtp):
        # Configure the mock so it doesn't raise any exception
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("<p>Test</p>", "Test Subject", "test@example.com")
        self.assertTrue(result)
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_auth_error(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"Authentication failed")
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("<p>Test</p>", "Test Subject", "test@example.com")
        self.assertFalse(result)

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_smtp_error(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPException("Some SMTP error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("<p>Test</p>", "Test Subject", "test@example.com")
        self.assertFalse(result)

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_email_general_exception(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("General error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email("<p>Test</p>", "Test Subject", "test@example.com")
        self.assertFalse(result)

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_failure_notify_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Does not return anything, but shouldn't raise exception
        send_failure_notify("Test error message", "test@example.com")
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()

    @patch('email_sender.smtplib.SMTP_SSL')
    def test_send_failure_notify_exception(self, mock_smtp):
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("General error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Should catch the exception and not propagate it
        send_failure_notify("Test error message", "test@example.com")

if __name__ == '__main__':
    unittest.main()
