from PySide6 import QtWidgets
from PySide6.QtCore import QObject, QCoreApplication
from .icon_manager import IconManager


class TrayIconManager(QObject):
    def __init__(self, settings_callback, exit_callback):
        super().__init__()
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(IconManager.get_tray_icon())
        self.tray.setToolTip(QCoreApplication.translate("TrayIcon", "LiteOCR - Ready"))

        menu = QtWidgets.QMenu()
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
        settings_action = menu.addAction(
            IconManager.get_settings_icon(),
            QCoreApplication.translate("TrayIcon", "Settings"),
        )
        if settings_action:
            settings_action.triggered.connect(settings_callback)

        exit_action = menu.addAction(
            IconManager.get_exit_icon(), QCoreApplication.translate("TrayIcon", "Exit")
        )
        if exit_action:
            exit_action.triggered.connect(exit_callback)

        self.tray.setContextMenu(menu)

    def show(self):
        """Shows the tray icon."""
        self.tray.show()

    def show_message(self, title, message, icon_name="icon"):
        """Displays a message from the tray icon.
        Note: title and message should be translated by the caller.
        """
        self.tray.showMessage(title, message, IconManager.get_icon(icon_name))
