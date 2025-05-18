from PySide6 import QtCore


class ConfigManager:
    def __init__(self, organization="LiteOCR", application="LiteOCR"):
        self.settings = QtCore.QSettings(organization, application)

    def load_config(self):
        """Loads configuration from QSettings."""
        return {
            "api_key": self.settings.value("api_key", ""),
            "model": self.settings.value("model", "gpt-4.1-mini"),
            "base_url": self.settings.value("base_url", ""),
        }

    def save_config(self, config):
        """Saves configuration to QSettings."""
        self.settings.setValue("api_key", config.get("api_key", ""))
        self.settings.setValue("model", config.get("model", "gpt-4.1-mini"))
        self.settings.setValue("base_url", config.get("base_url", ""))

    def get_api_key(self):
        """Gets the API key from the current settings."""
        return self.settings.value("api_key", "")

    def get_model(self):
        """Gets the model from the current settings."""
        return self.settings.value("model", "gpt-4.1-mini")

    def get_base_url(self):
        """Gets the base URL from the current settings."""
        return self.settings.value("base_url", "")
