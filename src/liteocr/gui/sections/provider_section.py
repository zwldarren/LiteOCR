from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal as QSignal
from ..widgets import StyledLineEdit, StyledComboBox, SectionFrame


class ProviderSection(SectionFrame):
    """Handles provider configuration UI and logic."""

    provider_changed = QSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent.tr("Provider Settings"))
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Initialize provider configuration components."""
        self.content_layout.addWidget(QLabel(self.parent.tr("Provider:")), 0, 0)
        self.provider_combo = StyledComboBox()
        self.provider_combo.addItems(["openai", "openai-compatible", "gemini"])
        self.provider_combo.currentTextChanged.connect(self.provider_changed)
        self.content_layout.addWidget(self.provider_combo, 0, 1)

        self.content_layout.addWidget(QLabel(self.parent.tr("LLM API Key:")), 1, 0)
        self.api_key_input = StyledLineEdit(self.parent.tr("Enter your API key"))
        self.content_layout.addWidget(self.api_key_input, 1, 1)

        self.content_layout.addWidget(QLabel(self.parent.tr("Model:")), 2, 0)
        self.model_input = StyledLineEdit(
            self.parent.tr("Enter model name (e.g. gpt-4.1-mini)")
        )
        self.content_layout.addWidget(self.model_input, 2, 1)

        self.base_url_label = QLabel(self.parent.tr("API Base URL:"))
        self.content_layout.addWidget(self.base_url_label, 3, 0)
        self.base_url_input = StyledLineEdit(self.parent.tr("Enter custom API endpoint"))
        self.content_layout.addWidget(self.base_url_input, 3, 1)

    def update_ui_visibility(self):
        """Updates UI element visibility based on provider selection."""
        show_base_url = self.provider_combo.currentText() == "openai-compatible"
        self.base_url_label.setVisible(show_base_url)
        self.base_url_input.setVisible(show_base_url)

    def set_values(self, config):
        """Sets the values from a config dictionary."""
        self.api_key_input.setText(config["api_key"])
        self.provider_combo.setCurrentText(config.get("provider", "openai"))
        self.base_url_input.setText(config["base_url"])
        self.model_input.setText(config["model"])

    def get_values(self):
        """Returns the current values as a dictionary."""
        return {
            "api_key": self.api_key_input.text(),
            "provider": self.provider_combo.currentText(),
            "base_url": self.base_url_input.text(),
            "model": self.model_input.text()
        }
