from PySide6 import QtWidgets
from PySide6.QtCore import QObject, QCoreApplication
from .icon_manager import IconManager
from .common.menu_builder import MenuBuilder


class TrayIconManager(QObject):
    def __init__(self, settings_callback, exit_callback):
        super().__init__()
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(IconManager.get_tray_icon())
        self.tray.setToolTip(QCoreApplication.translate("TrayIcon", "LiteOCR - Ready"))

        menu = MenuBuilder.build_menu()

        self.settings_action = MenuBuilder.add_action(
            menu, "Settings", IconManager.get_settings_icon(), settings_callback
        )

        MenuBuilder.add_separator(menu)

        self.exit_action = MenuBuilder.add_action(
            menu, "Exit", IconManager.get_exit_icon(), exit_callback
        )

        self.tray.setContextMenu(menu)

    def show(self):
        """Shows the tray icon."""
        self.tray.show()

    def show_message(self, title, message, icon_name="icon"):
        """Displays a message from the tray icon.
        Note: title and message should be translated by the caller.
        """
        self.tray.showMessage(title, message, IconManager.get_icon(icon_name))

    def update_texts(self):
        """Updates translatable texts for the tray icon and menu."""
        self.tray.setToolTip(QCoreApplication.translate("TrayIcon", "LiteOCR - Ready"))
        if self.settings_action:
            self.settings_action.setText(
                QCoreApplication.translate("TrayIcon", "Settings")
            )
        if self.exit_action:
            self.exit_action.setText(QCoreApplication.translate("TrayIcon", "Exit"))
