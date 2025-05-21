from PySide6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QWidget,
    QStyledItemDelegate,
    QListView,
)
from PySide6.QtCore import Property, QSize


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText(placeholder_text)


class StyledComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._rounded = True
        self.setProperty("rounded", True)

        self.setView(QListView())

        self.setItemDelegate(QStyledItemDelegate())

        self._icon_size = QSize(16, 16)
        self.setIconSize(self._icon_size)

        self.setup_arrow_icon()

    def setup_arrow_icon(self):
        pass

    def showPopup(self):
        super().showPopup()
        popup = self.findChild(QFrame)
        if popup:
            popup.setMinimumWidth(self.width())

    def _get_rounded(self):
        return self._rounded

    def _set_rounded(self, value):
        if self._rounded != value:
            self._rounded = value
            self.setProperty("rounded", value)
            self.style().polish(self)

    rounded = Property(bool, _get_rounded, _set_rounded)


class StyledButton(QPushButton):
    def __init__(self, text, primary=False, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self._primary = primary
        self.setProperty("primary", primary)

    # Define a Qt property for 'primary'
    def _get_primary(self):
        return self._primary

    def _set_primary(self, value):
        if self._primary != value:
            self._primary = value
            self.setProperty("primary", value)
            self.style().polish(self)

    primary = Property(bool, _get_primary, _set_primary)


class SectionFrame(QFrame):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        self.layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        self.content = QWidget()
        self.content_layout = QGridLayout(self.content)
        self.content_layout.setContentsMargins(0, 10, 0, 0)
        self.content_layout.setSpacing(10)
        self.layout.addWidget(self.content)
