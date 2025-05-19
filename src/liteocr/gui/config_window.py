from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QGridLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from .icon_manager import IconManager


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 8px;
                background-color: #2A2A2A;
                color: #E0E0E0;
                selection-background-color: #0078D7;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
            }
            QLineEdit:hover {
                background-color: #323232;
            }
        """)


class StyledComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 8px;
                background-color: #2A2A2A;
                color: #E0E0E0;
                min-height: 20px;
            }
            QComboBox:hover {
                background-color: #323232;
            }
            QComboBox:focus {
                border: 1px solid #0078D7;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #3C3C3C;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: "";
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #3C3C3C;
                selection-background-color: #0078D7;
                background-color: #2A2A2A;
                color: #E0E0E0;
            }
        """)


class StyledButton(QPushButton):
    def __init__(self, text, primary=False, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1084E0;
                }
                QPushButton:pressed {
                    background-color: #006CC1;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3C3C3C;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #4A4A4A;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
            """)


class SectionFrame(QFrame):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            SectionFrame {
                background-color: #252525;
                border-radius: 6px;
                margin: 5px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #3C3C3C;")
        self.layout.addWidget(separator)

        self.content = QWidget()
        self.content_layout = QGridLayout(self.content)
        self.content_layout.setContentsMargins(0, 10, 0, 0)
        self.content_layout.setSpacing(10)
        self.layout.addWidget(self.content)


class ConfigWindow(QDialog):
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("LiteOCR Settings"))
        self.setMinimumSize(500, 450)
        self.config_manager = config_manager

        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_pixmap = IconManager.get_tray_icon().pixmap(32, 32)
        if not icon_pixmap.isNull():
            icon_label.setPixmap(
                icon_pixmap.scaled(
                    32,
                    32,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        header_layout.addWidget(icon_label)

        title_label = QLabel(self.tr("LiteOCR Settings"))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Provider settings
        provider_section = SectionFrame(self.tr("Provider Settings"))
        provider_section.content_layout.addWidget(QLabel(self.tr("Provider:")), 0, 0)
        self.provider_combo = StyledComboBox()
        self.provider_combo.addItems(["openai", "openai-compatible", "gemini"])
        self.provider_combo.currentTextChanged.connect(self._update_ui_visibility)
        provider_section.content_layout.addWidget(self.provider_combo, 0, 1)

        provider_section.content_layout.addWidget(QLabel(self.tr("LLM API Key:")), 1, 0)
        self.api_key_input = StyledLineEdit(self.tr("Enter your API key"))
        provider_section.content_layout.addWidget(self.api_key_input, 1, 1)

        provider_section.content_layout.addWidget(QLabel(self.tr("Model:")), 2, 0)
        self.model_input = StyledLineEdit(
            self.tr("Enter model name (e.g. gpt-4.1-mini)")
        )
        provider_section.content_layout.addWidget(self.model_input, 2, 1)

        self.base_url_label = QLabel(self.tr("API Base URL:"))
        provider_section.content_layout.addWidget(self.base_url_label, 3, 0)
        self.base_url_input = StyledLineEdit(self.tr("Enter custom API endpoint"))
        provider_section.content_layout.addWidget(self.base_url_input, 3, 1)

        main_layout.addWidget(provider_section)

        # Shortcut settings
        shortcut_section = SectionFrame(self.tr("Shortcut Settings"))
        shortcut_section.content_layout.addWidget(
            QLabel(self.tr("Screenshot Shortcut:")), 0, 0
        )
        self.shortcut_input = StyledLineEdit()
        self.shortcut_input.setText("Ctrl+Alt+S")
        self.shortcut_input.setReadOnly(True)
        shortcut_section.content_layout.addWidget(self.shortcut_input, 0, 1)

        main_layout.addWidget(shortcut_section)

        main_layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_button = StyledButton(self.tr("Cancel"))
        button_layout.addWidget(self.cancel_button)
        self.save_button = StyledButton(self.tr("Save"), primary=True)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        self._update_ui_visibility()

        # Connect signals
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self._save_config)

        # Load current config if available
        if config_manager:
            config = config_manager.load_config()
            self.api_key_input.setText(config["api_key"])
            self.provider_combo.setCurrentText(config.get("provider", "openai"))
            self.base_url_input.setText(config["base_url"])
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

            # Initialize empty custom models
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
