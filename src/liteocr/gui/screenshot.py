from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap, QGuiApplication, QCursor
from PySide6.QtCore import Qt, QRect, Signal, QPoint
import logging
from enum import Enum


class DragMode(Enum):
    NoDrag = 0
    Move = 1
    ResizeTopLeft = 2
    ResizeTop = 3
    ResizeTopRight = 4
    ResizeRight = 5
    ResizeBottomRight = 6
    ResizeBottom = 7
    ResizeBottomLeft = 8
    ResizeLeft = 9


class ScreenshotOverlay(QWidget):
    selection_captured = Signal(QPixmap)
    overlay_closed = Signal()

    HANDLE_SIZE = 8
    MIN_RECT_SIZE = 20

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMouseTracking(True)

        current_screen = QGuiApplication.screenAt(QCursor.pos())
        if current_screen:
            screen_geometry = current_screen.geometry()
            self.setGeometry(screen_geometry)
        else:
            # Fallback if screen info is not available or problematic
            logging.warning(
                "Could not determine current screen geometry. Falling back to primary screen full-screen."
            )
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        self.selection_rect = QRect()
        self.drag_start_pos = QPoint()
        self.drag_mode = DragMode.NoDrag
        self.original_rect = QRect()  # Store original rect for resizing/moving

        self.is_selecting = False  # True when initially drawing a new rectangle

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position().toPoint()

            if self.selection_rect.isValid():
                # Check if resizing or moving existing rectangle
                self.drag_mode = self._get_drag_mode(self.drag_start_pos)
                if self.drag_mode != DragMode.NoDrag:
                    self.original_rect = self.selection_rect
                else:
                    # Start new selection if clicking outside existing rect
                    self.is_selecting = True
                    self.selection_rect = QRect(
                        self.drag_start_pos, self.drag_start_pos
                    )
            else:
                # Start new selection if no rect exists
                self.is_selecting = True
                self.selection_rect = QRect(self.drag_start_pos, self.drag_start_pos)
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        current_pos = event.position().toPoint()

        if self.is_selecting:
            # Drawing a new rectangle
            self.selection_rect = QRect(self.drag_start_pos, current_pos).normalized()
        elif self.drag_mode != DragMode.NoDrag:
            # Moving or resizing existing rectangle
            delta = current_pos - self.drag_start_pos
            new_rect = QRect(self.original_rect)

            if self.drag_mode == DragMode.Move:
                new_rect.translate(delta)
            elif self.drag_mode == DragMode.ResizeTopLeft:
                new_rect.setTopLeft(self.original_rect.topLeft() + delta)
            elif self.drag_mode == DragMode.ResizeTop:
                new_rect.setTop(self.original_rect.top() + delta.y())
            elif self.drag_mode == DragMode.ResizeTopRight:
                new_rect.setTopRight(self.original_rect.topRight() + delta)
            elif self.drag_mode == DragMode.ResizeRight:
                new_rect.setRight(self.original_rect.right() + delta.x())
            elif self.drag_mode == DragMode.ResizeBottomRight:
                new_rect.setBottomRight(self.original_rect.bottomRight() + delta)
            elif self.drag_mode == DragMode.ResizeBottom:
                new_rect.setBottom(self.original_rect.bottom() + delta.y())
            elif self.drag_mode == DragMode.ResizeBottomLeft:
                new_rect.setBottomLeft(self.original_rect.bottomLeft() + delta)
            elif self.drag_mode == DragMode.ResizeLeft:
                new_rect.setLeft(self.original_rect.left() + delta.x())

            # Ensure minimum size
            if new_rect.width() < self.MIN_RECT_SIZE:
                if self.drag_mode in [
                    DragMode.ResizeLeft,
                    DragMode.ResizeTopLeft,
                    DragMode.ResizeBottomLeft,
                ]:
                    new_rect.setLeft(new_rect.right() - self.MIN_RECT_SIZE)
                elif self.drag_mode in [
                    DragMode.ResizeRight,
                    DragMode.ResizeTopRight,
                    DragMode.ResizeBottomRight,
                ]:
                    new_rect.setRight(new_rect.left() + self.MIN_RECT_SIZE)
            if new_rect.height() < self.MIN_RECT_SIZE:
                if self.drag_mode in [
                    DragMode.ResizeTop,
                    DragMode.ResizeTopLeft,
                    DragMode.ResizeTopRight,
                ]:
                    new_rect.setTop(new_rect.bottom() - self.MIN_RECT_SIZE)
                elif self.drag_mode in [
                    DragMode.ResizeBottom,
                    DragMode.ResizeBottomLeft,
                    DragMode.ResizeBottomRight,
                ]:
                    new_rect.setBottom(new_rect.top() + self.MIN_RECT_SIZE)

            self.selection_rect = new_rect.normalized()

        self.setCursor(self._get_cursor_for_position(current_pos))
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_selecting:
                self.is_selecting = False
                self.selection_rect = QRect(
                    self.drag_start_pos, event.position().toPoint()
                ).normalized()
                if (
                    self.selection_rect.width() < self.MIN_RECT_SIZE
                    or self.selection_rect.height() < self.MIN_RECT_SIZE
                ):
                    self.selection_rect = QRect()  # Clear selection if too small

            self.drag_mode = DragMode.NoDrag
            self.setCursor(Qt.CursorShape.ArrowCursor)  # Reset cursor

            if self.selection_rect.isValid():
                captured_pixmap = self._capture_selection()
                if captured_pixmap:
                    self.selection_captured.emit(captured_pixmap)
                self.close()  # Close after capturing

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw semi-transparent overlay over the entire screen
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        # Draw selection rectangle and handles if valid
        if self.selection_rect.isValid():
            # Clear the selected area (make it transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self.selection_rect, Qt.GlobalColor.transparent)
            painter.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_SourceOver
            )

            # Draw border
            pen = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)

            # Draw resize handles
            handle_color = QColor(0, 120, 215)  # Blue handles
            painter.setBrush(handle_color)
            painter.setPen(Qt.NoPen)

            # Corners
            painter.drawRect(self._get_handle_rect(self.selection_rect.topLeft()))
            painter.drawRect(self._get_handle_rect(self.selection_rect.topRight()))
            painter.drawRect(self._get_handle_rect(self.selection_rect.bottomLeft()))
            painter.drawRect(self._get_handle_rect(self.selection_rect.bottomRight()))

            # Midpoints
            painter.drawRect(
                self._get_handle_rect(
                    self.selection_rect.center().x(), self.selection_rect.top()
                )
            )
            painter.drawRect(
                self._get_handle_rect(
                    self.selection_rect.center().x(), self.selection_rect.bottom()
                )
            )
            painter.drawRect(
                self._get_handle_rect(
                    self.selection_rect.left(), self.selection_rect.center().y()
                )
            )
            painter.drawRect(
                self._get_handle_rect(
                    self.selection_rect.right(), self.selection_rect.center().y()
                )
            )

    def _get_handle_rect(self, x_or_point, y=None):
        """Helper to get a handle rectangle from a point or x,y coordinates."""
        if isinstance(x_or_point, QPoint):
            point = x_or_point
        else:
            point = QPoint(x_or_point, y)
        return QRect(
            point.x() - self.HANDLE_SIZE // 2,
            point.y() - self.HANDLE_SIZE // 2,
            self.HANDLE_SIZE,
            self.HANDLE_SIZE,
        )

    def _get_drag_mode(self, pos: QPoint) -> DragMode:
        """Determines if the mouse is over a resize handle or inside the selection."""
        if not self.selection_rect.isValid():
            return DragMode.NoDrag

        # Check corners
        if self._get_handle_rect(self.selection_rect.topLeft()).contains(pos):
            return DragMode.ResizeTopLeft
        if self._get_handle_rect(self.selection_rect.topRight()).contains(pos):
            return DragMode.ResizeTopRight
        if self._get_handle_rect(self.selection_rect.bottomLeft()).contains(pos):
            return DragMode.ResizeBottomLeft
        if self._get_handle_rect(self.selection_rect.bottomRight()).contains(pos):
            return DragMode.ResizeBottomRight

        # Check midpoints
        if self._get_handle_rect(
            self.selection_rect.center().x(), self.selection_rect.top()
        ).contains(pos):
            return DragMode.ResizeTop
        if self._get_handle_rect(
            self.selection_rect.center().x(), self.selection_rect.bottom()
        ).contains(pos):
            return DragMode.ResizeBottom
        if self._get_handle_rect(
            self.selection_rect.left(), self.selection_rect.center().y()
        ).contains(pos):
            return DragMode.ResizeLeft
        if self._get_handle_rect(
            self.selection_rect.right(), self.selection_rect.center().y()
        ).contains(pos):
            return DragMode.ResizeRight

        # Check if inside the rectangle for moving
        if self.selection_rect.contains(pos):
            return DragMode.Move

        return DragMode.NoDrag

    def _get_cursor_for_position(self, pos: QPoint) -> Qt.CursorShape:
        """Returns the appropriate cursor shape based on mouse position."""
        mode = self._get_drag_mode(pos)
        if mode == DragMode.ResizeTopLeft or mode == DragMode.ResizeBottomRight:
            return Qt.CursorShape.SizeFDiagCursor
        elif mode == DragMode.ResizeTopRight or mode == DragMode.ResizeBottomLeft:
            return Qt.CursorShape.SizeBDiagCursor
        elif mode == DragMode.ResizeTop or mode == DragMode.ResizeBottom:
            return Qt.CursorShape.SizeVerCursor
        elif mode == DragMode.ResizeLeft or mode == DragMode.ResizeRight:
            return Qt.CursorShape.SizeHorCursor
        elif mode == DragMode.Move:
            return Qt.CursorShape.SizeAllCursor
        else:
            return Qt.CursorShape.CrossCursor  # Default for selection

    def _capture_selection(self):
        """Capture the selected area and return as QPixmap"""
        if not self.selection_rect.isValid():
            logging.warning("Selection rectangle is not valid for capture.")
            return None

        target_screen = self.screen()
        if not target_screen:
            logging.error("Could not determine target screen for capture from widget.")
            return None

        try:
            pixmap = target_screen.grabWindow(
                0,  # Capture the desktop content (Window ID 0)
                self.selection_rect.x(),
                self.selection_rect.y(),
                self.selection_rect.width(),
                self.selection_rect.height(),
            )
            if pixmap.isNull():
                logging.error("Captured pixmap is null.")
                return None
            return pixmap
        except Exception as e:
            logging.error(f"Error grabbing pixmap: {e}")
            return None

    def closeEvent(self, event):
        self.overlay_closed.emit()
        super().closeEvent(event)
