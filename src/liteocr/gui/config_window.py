from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from .icon_manager import IconManager
from .widgets import StyledButton
from .hotkey_recorder import HotkeyRecorder
from .sections.language_section import LanguageSection
from .sections.provider_section import ProviderSection
from .sections.shortcut_section import ShortcutSection
from .common.style_manager import StyleManager
import logging


class ConfigWindow(QDialog):
    hotkey_changed = Signal(str)

    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.setWindowTitle("LiteOCR")
        self.setMinimumSize(500, 700)
        self.config_manager = config_manager
        self.recording_hotkey = False
        self.recorded_keys = set()

        # Apply global styles
        StyleManager.apply_global_styles()

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

        # Language settings
        self.language_section = LanguageSection(self)
        main_layout.addWidget(self.language_section)

        # Provider settings
        self.provider_section = ProviderSection(self)
        self.provider_section.provider_changed.connect(self._update_ui_visibility)
        main_layout.addWidget(self.provider_section)

        # Shortcut settings
        self.shortcut_section = ShortcutSection(self)
        main_layout.addWidget(self.shortcut_section)

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

        # Initialize hotkey recorder
        self.hotkey_recorder = HotkeyRecorder()

        # Connect signals
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self._save_config)
        self.shortcut_section.connect_signals(self.hotkey_recorder)
        self.shortcut_section.hotkey_changed.connect(self.hotkey_changed)

        # Load current config if available
        if config_manager:
            config = config_manager.load_config()
            self.provider_section.set_values(config)
            self.shortcut_section.set_hotkey(config.get("hotkey", "<ctrl>+<alt>+s"))

            # Set language
            current_lang = config.get("language", "")
            self.language_section.set_language(current_lang)

        # Store initial hotkey to check for changes on save
        self._initial_hotkey = (
            config.get("hotkey", "<ctrl>+<alt>+s")
            if config_manager
            else "<ctrl>+<alt>+s"
        )

    def closeEvent(self, event):
        """Ensures the hotkey recorder is stopped when the window is closed."""
        if hasattr(self, "hotkey_recorder"):
            self.hotkey_recorder.stop_recording()
        super().closeEvent(event)

    def _update_ui_visibility(self):
        """Updates UI element visibility based on provider selection."""
        self.provider_section.update_ui_visibility()
        self.adjustSize()

    def _start_hotkey_recording(self):
        """Deprecated - recording is now handled by ShortcutSection"""
        pass

    def _on_recording_started(self):
        self.recording_hotkey = True
        self.recorded_keys = set()
        self.hotkey_status_label.setText(
            self.tr("Recording... Press your desired shortcut. Press ESC to cancel.")
        )
        self.hotkey_status_label.setStyleSheet("color: #FFA500; font-size: 10px;")

    def _on_key_pressed(self, key_str):
        if not self.recording_hotkey:
            return

        if key_str == "esc":
            if hasattr(self, "hotkey_recorder"):
                self.hotkey_recorder.stop_recording(cancelled=True)
            return

        self.recorded_keys.add(key_str)
        self._update_shortcut_display()

    def _on_recording_stopped(self, hotkey_str):
        self.recording_hotkey = False

        if not hotkey_str:
            self.hotkey_status_label.setText(
                self.tr("No hotkey recorded. Please try again.")
            )
            # Red for error
            self.hotkey_status_label.setStyleSheet("color: #FF0000; font-size: 10px;")
            # Restore previous hotkey if available
            config = self.config_manager.load_config()
            self.shortcut_input.setText(config.get("hotkey", "<ctrl>+<alt>+s"))
        else:
            self.shortcut_input.setText(hotkey_str)
            self.hotkey_status_label.setText(self.tr("Hotkey recorded successfully!"))
            self.hotkey_status_label.setStyleSheet(
                "color: #00FF00; font-size: 10px;"
            )  # Green for success

    def _update_shortcut_display(self):
        # Sort keys for consistent display
        sorted_keys = []
        if "<ctrl>" in self.recorded_keys:
            sorted_keys.append("<ctrl>")
        if "<shift>" in self.recorded_keys:
            sorted_keys.append("<shift>")
        if "<alt>" in self.recorded_keys:
            sorted_keys.append("<alt>")
        if "<cmd>" in self.recorded_keys:
            sorted_keys.append("<cmd>")

        # Add non-modifier keys
        non_modifiers = sorted(
            k
            for k in self.recorded_keys
            if not k.startswith("<")
            or k == "<f1>"
            or k == "<f2>"
            or k == "<f3>"
            or k == "<f4>"
            or k == "<f5>"
            or k == "<f6>"
            or k == "<f7>"
            or k == "<f8>"
            or k == "<f9>"
            or k == "<f10>"
            or k == "<f11>"
            or k == "<f12>"
        )
        sorted_keys.extend(non_modifiers)

        hotkey_str = "+".join(sorted_keys)
        self.shortcut_input.setText(hotkey_str)
        self.hotkey_status_label.setText(self.tr("Current shortcut: ") + hotkey_str)
        self.hotkey_status_label.setStyleSheet("color: #E0E0E0; font-size: 10px;")

    def _save_config(self):
        """Saves the current configuration."""
        if self.config_manager:
            config = self.provider_section.get_values()
            config.update(
                {
                    "language": self.language_section.get_selected_language(),
                    "hotkey": self.shortcut_section.get_hotkey(),
                    "custom_models": {},  # Initialize empty custom models
                }
            )

            self.config_manager.save_config(config)

            # Emit hotkey_changed signal if the hotkey has actually changed
            if self._initial_hotkey != config["hotkey"]:
                logging.info(
                    f"ConfigWindow: Hotkey changed from '{self._initial_hotkey}' to '{config['hotkey']}'. Emitting signal."
                )
                self._initial_hotkey = config["hotkey"]
                self.hotkey_changed.emit(config["hotkey"])
        self.accept()
