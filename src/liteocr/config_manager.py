from PySide6 import QtCore
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging


class ConfigManager:
    # Create a fixed salt value that is independent of the user
    SALT = b"LiteOCR-Secure-Salt-For-Config"

    def __init__(self, organization="LiteOCR", application="LiteOCR"):
        self.settings = QtCore.QSettings(organization, application)

        # Derive a key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.SALT,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"LiteOCR-Master-Key"))
        self.cipher = Fernet(key)

    def load_config(self):
        """Load configuration and decrypt sensitive fields"""
        config = {
            "provider": self.settings.value("provider", "openai"),
            "model": self.settings.value("model", "gpt-4.1-mini"),
            "base_url": self.settings.value("base_url", ""),
            "language": self.settings.value("language", ""),
            "hotkey": self.settings.value("hotkey", "<ctrl>+<alt>+s"),
        }

        # Load and decrypt the API key
        enc_api_key = self.settings.value("api_key", "")
        if enc_api_key:
            try:
                config["api_key"] = self.cipher.decrypt(enc_api_key.encode()).decode()
            except (InvalidToken, ValueError) as e:
                logging.error(f"API key decryption failed: {e}")
                config["api_key"] = ""
        else:
            config["api_key"] = ""

        return config

    def save_config(self, config):
        """Save configuration, encrypting sensitive fields"""
        # Encrypt and save the API key
        api_key = config.get("api_key", "")
        if api_key:
            enc_api_key = self.cipher.encrypt(api_key.encode()).decode()
            self.settings.setValue("api_key", enc_api_key)
        else:
            self.settings.setValue("api_key", "")

        # Save other fields
        self.settings.setValue("provider", config.get("provider", "openai"))
        self.settings.setValue("model", config.get("model", "gpt-4.1-mini"))
        self.settings.setValue("base_url", config.get("base_url", ""))
        self.settings.setValue("language", config.get("language", ""))
        self.settings.setValue("hotkey", config.get("hotkey", "<ctrl>+<alt>+s"))

    def get_api_key(self):
        """Safely retrieve the API key"""
        enc_api_key = self.settings.value("api_key", "")
        if not enc_api_key:
            return ""

        try:
            return self.cipher.decrypt(enc_api_key.encode()).decode()
        except (InvalidToken, ValueError) as e:
            logging.error(f"API key decryption failed: {e}")
            return ""

    def get_provider(self):
        """Retrieve the provider from the current settings."""
        return self.settings.value("provider", "openai")

    def get_model(self):
        """Retrieve the model from the current settings."""
        return self.settings.value("model", "gpt-4.1-mini")

    def get_base_url(self):
        """Retrieve the base URL from the current settings."""
        return self.settings.value("base_url", "")
