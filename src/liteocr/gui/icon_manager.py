from PySide6.QtGui import QIcon


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
        return QIcon(f":/icons/{name}.svg")

    @staticmethod
    def get_tray_icon() -> QIcon:
        return QIcon(":/icons/icon.svg")

    @staticmethod
    def get_settings_icon() -> QIcon:
        return QIcon(":/icons/icon-settings.svg")

    @staticmethod
    def get_exit_icon() -> QIcon:
        return QIcon(":/icons/exit-arrow.svg")

    @staticmethod
    def get_arrow_down_icon() -> QIcon:
        return QIcon(":/icons/arrow-down.svg")
