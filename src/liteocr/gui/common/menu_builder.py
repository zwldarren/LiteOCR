from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QCoreApplication


class MenuBuilder:
    """
    A utility class for building consistent QMenu instances.
    Centralizes menu styling and action creation.
    """

    @staticmethod
    def build_menu(parent=None) -> QMenu:
        """
        Creates and returns a styled QMenu instance.
        """
        menu = QMenu(parent)
        menu.setStyleSheet("""
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
        return menu

    @staticmethod
    def add_action(
        menu: QMenu, text_key: str, icon: QIcon = None, callback=None
    ) -> QAction:
        """
        Adds a styled action to the given menu.

        Args:
            menu: The QMenu to add the action to.
            text_key: The translation key for the action's text (e.g., "Settings").
            icon: The QIcon for the action (optional).
            callback: The function to connect to the action's triggered signal (optional).

        Returns:
            The created QAction object.
        """
        action = QAction(icon, QCoreApplication.translate("Menu", text_key), menu)
        if callback:
            action.triggered.connect(callback)
        menu.addAction(action)
        return action

    @staticmethod
    def add_separator(menu: QMenu):
        """
        Adds a separator to the given menu.
        """
        menu.addSeparator()
