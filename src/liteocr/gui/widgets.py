from PySide6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QWidget,
)


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 8px;
                background-color: #2A2A2A;
                color: #E0E0E0;
                selection-background-color: #0078D7;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
            }
            QLineEdit:hover {
                background-color: #323232;
            }
        """)


class StyledComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 8px;
                background-color: #2A2A2A;
                color: #E0E0E0;
                min-height: 20px;
            }
            QComboBox:hover {
                background-color: #323232;
            }
            QComboBox:focus {
                border: 1px solid #0078D7;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #3C3C3C;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: "";
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #3C3C3C;
                selection-background-color: #0078D7;
                background-color: #2A2A2A;
                color: #E0E0E0;
            }
        """)


class StyledButton(QPushButton):
    def __init__(self, text, primary=False, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1084E0;
                }
                QPushButton:pressed {
                    background-color: #006CC1;
                }
            """)
        else:
            self.setStyleSheet("""
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
            """)


class SectionFrame(QFrame):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            SectionFrame {
                background-color: #252525;
                border-radius: 6px;
                margin: 5px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #3C3C3C;")
        self.layout.addWidget(separator)

        self.content = QWidget()
        self.content_layout = QGridLayout(self.content)
        self.content_layout.setContentsMargins(0, 10, 0, 0)
        self.content_layout.setSpacing(10)
        self.layout.addWidget(self.content)
