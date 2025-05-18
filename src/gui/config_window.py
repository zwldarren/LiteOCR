from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
)


class ConfigWindow(QDialog):
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.setWindowTitle("LiteOCR Settings")
        self.setFixedSize(400, 300)
        self.config_manager = config_manager

        # Main layout
        layout = QVBoxLayout()

        # API Key Section
        layout.addWidget(QLabel("LLM API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key")
        layout.addWidget(self.api_key_input)

        # Model Selection
        layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-4.1-mini"])
        layout.addWidget(self.model_combo)

        # API Base URL
        layout.addWidget(QLabel("API Base URL:"))
        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText(
            "Leave empty for default OpenAI endpoint"
        )
        layout.addWidget(self.base_url_input)

        # Shortcut Settings
        layout.addWidget(QLabel("Screenshot Shortcut:"))
        self.shortcut_input = QLineEdit("Ctrl+Alt+S")
        self.shortcut_input.setReadOnly(True)
        layout.addWidget(self.shortcut_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect signals
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self._save_config)

        # Load current config if available
        if config_manager:
            config = config_manager.load_config()
            self.api_key_input.setText(config["api_key"])
            self.model_combo.setCurrentText(config["model"])
            self.base_url_input.setText(config["base_url"])

    def _save_config(self):
        """Saves the current configuration."""
        if self.config_manager:
            config = {
                "api_key": self.api_key_input.text(),
                "model": self.model_combo.currentText(),
                "base_url": self.base_url_input.text(),
            }
            self.config_manager.save_config(config)
        self.accept()
