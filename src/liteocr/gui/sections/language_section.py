from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QFont
from ..widgets import StyledComboBox, SectionFrame


class LanguageSection(SectionFrame):
    """Handles language selection UI and logic."""

    def __init__(self, parent=None):
        super().__init__(parent.tr("Language Settings"))
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Initialize language selection components."""
        self.content_layout.addWidget(QLabel(self.parent.tr("Language:")), 0, 0)
        self.language_combo = StyledComboBox()
        self.language_combo.addItems([
            "System Default", 
            "English (en_US)", 
            "简体中文 (zh_CN)"
        ])
        self.content_layout.addWidget(self.language_combo, 0, 1)

    def get_selected_language(self):
        """Returns the currently selected language code."""
        language_map = {
            "System Default": "",
            "English (en_US)": "en_US",
            "简体中文 (zh_CN)": "zh_CN",
        }
        return language_map[self.language_combo.currentText()]

    def set_language(self, language_code):
        """Sets the combo box to the specified language code."""
        language_map = {
            "": "System Default",
            "en_US": "English (en_US)",
            "zh_CN": "简体中文 (zh_CN)",
        }
        self.language_combo.setCurrentText(
            language_map.get(language_code, "System Default")
        )
