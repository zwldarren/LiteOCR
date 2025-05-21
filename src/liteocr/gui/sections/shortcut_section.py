from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from ..widgets import StyledLineEdit, StyledButton, SectionFrame


class ShortcutSection(SectionFrame):
    """Handles screenshot shortcut configuration UI and logic."""

    hotkey_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent.tr("Shortcut Settings"))
        self.parent = parent
        self._setup_ui()
        self._initial_hotkey = ""

    def _setup_ui(self):
        """Initialize shortcut configuration components."""
        self.content_layout.addWidget(
            QLabel(self.parent.tr("Screenshot Shortcut:")), 0, 0
        )
        self.shortcut_input = StyledLineEdit()
        self.shortcut_input.setReadOnly(True)
        self.content_layout.addWidget(self.shortcut_input, 0, 1)

        self.record_hotkey_button = StyledButton(self.parent.tr("Record Hotkey"))
        self.content_layout.addWidget(self.record_hotkey_button, 0, 2)

        self.hotkey_status_label = QLabel(
            self.parent.tr("Press 'Record Hotkey' to set a new shortcut.")
        )
        self.hotkey_status_label.setStyleSheet("color: #AAAAAA; font-size: 10px;")
        self.content_layout.addWidget(self.hotkey_status_label, 1, 0, 1, 3)

    def set_hotkey(self, hotkey):
        """Sets the current hotkey value."""
        self._initial_hotkey = hotkey
        self.shortcut_input.setText(hotkey)

    def get_hotkey(self):
        """Returns the current hotkey value."""
        return self.shortcut_input.text()

    def connect_signals(self, hotkey_recorder):
        """Connects signals from the hotkey recorder."""
        self.hotkey_recorder = hotkey_recorder
        self.record_hotkey_button.clicked.connect(self._start_recording)
        self.hotkey_recorder.recording_stopped.connect(self._on_recording_stopped)
        self.hotkey_recorder.key_pressed.connect(self._on_key_pressed)
        self.hotkey_recorder.recording_started.connect(self._on_recording_started)

    def _start_recording(self):
        """Starts the hotkey recording process."""
        self.hotkey_recorder.start_recording()

    def _on_recording_started(self):
        """Handles when recording starts."""
        self.hotkey_status_label.setText(
            self.parent.tr(
                "Recording... Press your desired shortcut. Press ESC to cancel."
            )
        )
        self.hotkey_status_label.setStyleSheet("color: #FFA500; font-size: 10px;")

    def _on_key_pressed(self, key_str):
        """Updates display during recording."""
        self.hotkey_status_label.setText(
            self.parent.tr("Recording... Current keys: ") + key_str
        )

    def _on_recording_stopped(self, hotkey_str):
        """Handles when hotkey recording is complete."""
        if not hotkey_str:
            self.hotkey_status_label.setText(
                self.parent.tr("No hotkey recorded. Please try again.")
            )
            self.hotkey_status_label.setStyleSheet("color: #FF0000; font-size: 10px;")
            self.shortcut_input.setText(self._initial_hotkey)
        else:
            self.shortcut_input.setText(hotkey_str)
            self.hotkey_status_label.setText(
                self.parent.tr("Hotkey recorded successfully!")
            )
            self.hotkey_status_label.setStyleSheet("color: #00FF00; font-size: 10px;")
            if self._initial_hotkey != hotkey_str:
                self.hotkey_changed.emit(hotkey_str)
