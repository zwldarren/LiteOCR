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

        # Provider Selection
        layout.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["openai", "openai-compatible", "gemini"])
        self.provider_combo.currentTextChanged.connect(self._update_ui_visibility)
        layout.addWidget(self.provider_combo)

        # API Key Section
        layout.addWidget(QLabel("LLM API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key")
        layout.addWidget(self.api_key_input)

        # Model Selection
        layout.addWidget(QLabel("Model:"))
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Enter model name (e.g. gpt-4.1-mini)")
        layout.addWidget(self.model_input)

        # API Base URL
        self.base_url_label = QLabel("API Base URL:")
        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("Enter custom API endpoint")
        layout.addWidget(self.base_url_label)
        layout.addWidget(self.base_url_input)
        self._update_ui_visibility()  # Set initial visibility

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
            self.provider_combo.setCurrentText(config.get("provider", "openai"))
            self.base_url_input.setText(config["base_url"])
            # Set initial model value
            self.model_input.setText(config["model"])

    def _update_ui_visibility(self):
        """Updates UI element visibility based on provider selection."""
        show_base_url = self.provider_combo.currentText() == "openai-compatible"
        self.base_url_label.setVisible(show_base_url)
        self.base_url_input.setVisible(show_base_url)

    def _save_config(self):
        """Saves the current configuration."""
        if self.config_manager:
            # Get current model and provider
            current_model = self.model_input.text()
            current_provider = self.provider_combo.currentText()

            # Initialize empty custom models (we no longer track them separately)
            custom_models = {}

            config = {
                "api_key": self.api_key_input.text(),
                "provider": current_provider,
                "model": current_model,
                "base_url": self.base_url_input.text(),
                "custom_models": custom_models,
            }
            self.config_manager.save_config(config)
        self.accept()
