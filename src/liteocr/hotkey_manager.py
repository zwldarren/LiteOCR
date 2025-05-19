import logging
from pynput import keyboard
from PySide6.QtCore import QThread, Signal as QSignal, Slot


class HotkeyListenerThread(QThread):
    hotkey_activated = QSignal()

    def __init__(self, hotkey_str, parent=None):
        super().__init__(parent)
        self.hotkey_str = hotkey_str
        self.listener = None
        self._is_running = True

    def run(self):
        logging.info(f"Hotkey listener thread started for: {self.hotkey_str}")
        try:
            self.listener = keyboard.GlobalHotKeys({self.hotkey_str: self._on_activate})
            self.listener.start()
            while self._is_running and self.listener.is_alive():
                self.msleep(100)
        except Exception as e:
            logging.error(f"Failed to start hotkey listener in thread: {e}")
        finally:
            if self.listener and self.listener.is_alive():
                self.listener.stop()
            logging.debug("Hotkey listener thread finished.")

    def _on_activate(self):
        logging.info(f"Hotkey {self.hotkey_str} activated.")
        self.hotkey_activated.emit()

    @Slot()
    def stop_listener(self):
        self._is_running = False
        if self.listener:
            self.listener.stop()
        self.quit()
        self.wait()
        logging.debug("Hotkey listener stopped.")
