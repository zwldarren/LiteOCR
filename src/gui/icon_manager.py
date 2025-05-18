from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile


class IconManager:
    """
    Manages all icon resources used in the application
    """

    @staticmethod
    def get_icon(name: str) -> QIcon:
        """
        Get icon by name

        Args:
            name: Icon name (without .svg extension)

        Returns:
            QIcon object
        """
        icon_path = f"resources/{name}.svg"
        if QFile.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()

    @staticmethod
    def get_tray_icon() -> QIcon:
        return IconManager.get_icon("icon")

    @staticmethod
    def get_settings_icon() -> QIcon:
        return IconManager.get_icon("icon-settings")

    @staticmethod
    def get_exit_icon() -> QIcon:
        return IconManager.get_icon("exit-arrow")

    @staticmethod
    def get_arrow_down_icon() -> QIcon:
        return IconManager.get_icon("arrow-down")
