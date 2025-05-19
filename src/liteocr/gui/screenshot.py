from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtCore import Qt, QRect, Signal


class ScreenshotOverlay(QWidget):
    selection_captured = Signal(QPixmap)
    overlay_closed = Signal()  # New signal

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        self.start_pos = None
        self.end_pos = None
        self.is_selecting = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.position().toPoint()
            self.end_pos = self.start_pos
            self.is_selecting = True
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.is_selecting = False
            captured_pixmap = self._capture_selection()
            if captured_pixmap:
                self.selection_captured.emit(captured_pixmap)
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        # Draw selection rectangle
        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.fillRect(rect, QColor(0, 0, 0, 0))

            pen = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen)
            painter.drawRect(rect)
        # else:

    def _capture_selection(self):
        """Capture the selected area and return as QPixmap"""
        # Get the screen where the overlay window is currently shown
        screen = self.screen()
        if not screen:
            screen = QApplication.primaryScreen()
            if not screen:
                return None

        if not self.start_pos or not self.end_pos:
            return None

        rect = QRect(self.start_pos, self.end_pos).normalized()
        return screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())

    def closeEvent(self, event):
        self.overlay_closed.emit()
        super().closeEvent(event)
