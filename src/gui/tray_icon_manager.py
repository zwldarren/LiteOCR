from PySide6 import QtWidgets, QtGui


class TrayIconManager:
    def __init__(self, settings_callback, exit_callback):
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon("icon.svg"))
        self.tray.setToolTip("LiteOCR - Ready")

        menu = QtWidgets.QMenu()
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(settings_callback)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(exit_callback)

        self.tray.setContextMenu(menu)

    def show(self):
        """Shows the tray icon."""
        self.tray.show()

    def show_message(self, title, message, icon_path="icon.svg", duration=2000):
        """Displays a message from the tray icon."""
        self.tray.showMessage(title, message, QtGui.QIcon(icon_path), duration)
