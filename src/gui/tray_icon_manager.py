from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QObject, QCoreApplication


class TrayIconManager(QObject):
    def __init__(self, settings_callback, exit_callback):
        super().__init__()
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon("icon.svg"))
        self.tray.setToolTip(QCoreApplication.translate("TrayIcon", "LiteOCR - Ready"))

        menu = QtWidgets.QMenu()
        settings_action = menu.addAction(QCoreApplication.translate("TrayIcon", "Settings"))
        settings_action.triggered.connect(settings_callback)
        exit_action = menu.addAction(QCoreApplication.translate("TrayIcon", "Exit"))
        exit_action.triggered.connect(exit_callback)

        self.tray.setContextMenu(menu)

    def show(self):
        """Shows the tray icon."""
        self.tray.show()

    def show_message(self, title, message, icon_path="icon.svg"):
        """Displays a message from the tray icon.
        Note: title and message should be translated by the caller.
        """
        self.tray.showMessage(title, message, QtGui.QIcon(icon_path))
