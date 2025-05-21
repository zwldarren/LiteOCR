from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor


class StyleManager:
    """
    Manages application-wide UI styling.
    Centralizes common styles to ensure consistency.
    """

    @staticmethod
    def apply_global_styles():
        """Applies a consistent dark theme to the entire application."""
        app = QApplication.instance()
        if not app:
            return

        app.setStyleSheet("""
            /* Labels */
            QLabel {
                color: #E0E0E0;
            }

            /* Buttons */
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

            QPushButton[primary="true"] {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton[primary="true"]:hover {
                background-color: #1084E0;
            }
            QPushButton[primary="true"]:pressed {
                background-color: #006CC1;
            }

            /* LineEdits */
            QLineEdit {
                border: 1px solid #606060;
                border-radius: 4px;
                padding: 8px;
                background-color: #333333;
                color: #E0E0E0;
                selection-background-color: #0078D7;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
            }
            QLineEdit:hover {
                background-color: #323232;
            }

            /* ComboBoxes */
            QComboBox {
                border: 1px solid #606060;
                border-radius: 4px;
                padding: 8px 30px 8px 8px;
                background-color: #333333;
                color: #E0E0E0;
                min-height: 20px;
                selection-background-color: #0078D7;
                selection-color: white;
                text-align: left;
            }
            QComboBox:hover {
                background-color: #323232;
                border: 1px solid #707070;
            }
            QComboBox:focus {
                border: 1px solid #0078D7;
            }
            QComboBox:disabled {
                background-color: #252525;
                color: #808080;
                border: 1px solid #404040;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border-left-width: 0px;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                margin-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/arrow-down.svg);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                selection-background-color: #0078D7;
                background-color: #2A2A2A;
                color: #E0E0E0;
                outline: none;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 24px;
                padding: 4px 8px;
                border-radius: 2px;
                margin: 2px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #0078D7;
                color: white;
            }
            QComboBox QAbstractItemView::item:hover:!selected {
                background-color: #3A3A3A;
            }
            /* 为StyledComboBox添加特殊样式 */
            StyledComboBox[rounded="true"] {
                border-radius: 6px;
            }
            StyledComboBox[rounded="true"]::drop-down {
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            /* SectionFrame (Custom QFrame) */
            SectionFrame {
                background-color: #252525;
                border-radius: 6px;
                margin: 5px;
            }
            SectionFrame QLabel {
                color: #E0E0E0;
                font-weight: bold;
                font-size: 14px;
            }
            SectionFrame QFrame[frameShape="4"] {
                height: 1px;
                background-color: #3C3C3C;
            }

            /* QDialog (for ConfigWindow) */
            QDialog {
                background-color: #1E1E1E;
                color: #E0E0E0;
            }

            /* QMenu (for TrayIconManager) */
            QMenu {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3C3C3C;
                border-radius: 6px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 30px 8px 15px;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #0078D7;
                color: white;
            }
            QMenu::item:hover:!selected {
                background-color: #2A2A2A;
            }
            QMenu::separator {
                height: 1px;
                background-color: #3C3C3C;
                margin: 6px 10px;
            }
            QMenu::icon {
                padding-right: 8px;
            }
        """)

    @staticmethod
    def get_text_color() -> QColor:
        """Returns the standard text color."""
        return QColor("#E0E0E0")

    @staticmethod
    def get_background_color() -> QColor:
        """Returns the standard background color."""
        return QColor("#1E1E1E")

    @staticmethod
    def get_accent_color() -> QColor:
        """Returns the primary accent color."""
        return QColor("#0078D7")

    @staticmethod
    def get_border_color() -> QColor:
        """Returns the standard border color."""
        return QColor("#3C3C3C")

    @staticmethod
    def get_hover_color() -> QColor:
        """Returns the hover background color for interactive elements."""
        return QColor("#2A2A2A")
