from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QTranslator, QLibraryInfo
from gui.config_window import ConfigWindow
from gui.screenshot import ScreenshotOverlay
from ocr_processor import OCRProcessor
from config_manager import ConfigManager
from gui.tray_icon_manager import TrayIconManager
import pyperclip
from pynput import keyboard
from PySide6.QtCore import QThread, Signal as QSignal


class OCRWorker(QThread):
    finished = QSignal(str)
    error = QSignal(str)

    def __init__(self, ocr_processor, screenshot_pixmap):
        super().__init__()
        self.ocr_processor = ocr_processor
        self.screenshot_pixmap = screenshot_pixmap

    def run(self):
        try:
            image_bytes = self.ocr_processor.image_to_bytes(self.screenshot_pixmap)
            latex_text = self.ocr_processor.process_image(image_bytes)
            self.finished.emit(latex_text)
        except Exception as e:
            self.error.emit(str(e))


class LiteOCRApp(QtCore.QObject):
    hotkey_triggered = QtCore.Signal()
    app: QtWidgets.QApplication

    def __init__(self):
        super().__init__()

        # Ensure QApplication instance exists
        _app_instance = QtWidgets.QApplication.instance()
        if isinstance(_app_instance, QtWidgets.QApplication):
            self.app = _app_instance
        else:
            self.app = QtWidgets.QApplication([])

        # Load translations
        self.qt_translator = QTranslator()
        if self.qt_translator.load(
            "qt_" + QtCore.QLocale().name(),
            QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
        ):
            self.app.installTranslator(self.qt_translator)

        self.app_translator = QTranslator()
        locale = QtCore.QLocale()
        lang = locale.name()
        lang = "zh_CN"

        # try loading the translation files in different locations
        if self.app_translator.load(f"translations/liteocr_{lang}.qm"):
            self.app.installTranslator(self.app_translator)
        elif self.app_translator.load(f":/translations/liteocr_{lang}"):
            self.app.installTranslator(self.app_translator)
        elif self.app_translator.load(f"liteocr_{lang}", "translations"):
            self.app.installTranslator(self.app_translator)
        else:
            print(
                f"Warning: Could not load application translation file for language {lang}"
            )

        self.app.setQuitOnLastWindowClosed(False)

        self.config_manager = ConfigManager()
        self.tray_icon_manager = TrayIconManager(
            settings_callback=self.show_settings, exit_callback=self.app.quit
        )
        self.tray_icon_manager.show()
        self.ocr_processor = None

        # Initialize OCRProcessor if config is available
        initial_config = self.config_manager.load_config()
        if initial_config.get("api_key"):
            self.ocr_processor = OCRProcessor(
                str(initial_config["api_key"]),
                str(initial_config["model"]),
                str(initial_config["base_url"]),
            )

        self.screenshot_overlay = None

        # Setup pynput global hotkey
        self.hotkey_listener = keyboard.GlobalHotKeys(
            {"<ctrl>+<alt>+s": self._on_hotkey_activated}
        )
        self.hotkey_listener.start()

        # Connect application aboutToQuit signal to stop the hotkey listener
        self.app.aboutToQuit.connect(self.hotkey_listener.stop)

        # Connect the custom signal to the slot
        self.hotkey_triggered.connect(self.capture_and_process)

    def _on_hotkey_activated(self):
        """Callback for pynput hotkey activation."""
        self.hotkey_triggered.emit()

    def capture_and_process(self):
        if not self.ocr_processor:
            self.tray_icon_manager.show_message(
                self.tr("LiteOCR Error"),
                self.tr("Please configure API key first"),
                "icon.svg",
            )
            return

        # Create and show the screenshot overlay
        self.screenshot_overlay = ScreenshotOverlay()
        self.screenshot_overlay.selection_captured.connect(
            self._process_captured_screenshot
        )
        self.screenshot_overlay.show()
        self.screenshot_overlay.activateWindow()
        self.screenshot_overlay.raise_()

    def _process_captured_screenshot(self, screenshot_pixmap):
        """Handles the captured screenshot pixmap asynchronously."""
        if not screenshot_pixmap:
            return

        if not self.ocr_processor:
            self.tray_icon_manager.show_message(
                self.tr("LiteOCR Error"),
                self.tr("OCR processor not initialized. Please check your API key."),
                "icon.svg",
            )
            return

        # Create and start worker thread
        self.worker = OCRWorker(self.ocr_processor, screenshot_pixmap)
        self.worker.finished.connect(self._on_ocr_finished)
        self.worker.error.connect(self._on_ocr_error)
        self.worker.start()

    def _on_ocr_finished(self, latex_text):
        """Handles successful OCR completion."""
        pyperclip.copy(latex_text)
        self.tray_icon_manager.show_message(
            self.tr("LiteOCR"), self.tr("LaTeX copied to clipboard!"), "icon.svg"
        )

    def _on_ocr_error(self, error_msg):
        """Handles OCR processing errors."""
        self.tray_icon_manager.show_message(
            self.tr("LiteOCR Error"),
            self.tr("Failed to process image: ") + error_msg,
            "icon.svg",
        )

    def show_settings(self):
        config_window = ConfigWindow(config_manager=self.config_manager)
        result = config_window.exec()

        # If settings were saved, reinitialize OCRProcessor with new config
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            current_config = self.config_manager.load_config()
            if current_config.get("api_key"):
                self.ocr_processor = OCRProcessor(
                    str(current_config["api_key"]),
                    str(current_config["model"]),
                    str(current_config["base_url"]),
                )
            else:
                self.ocr_processor = None  # Clear processor if API key is removed

    def run(self):
        self.app.exec()


if __name__ == "__main__":
    ocr_app = LiteOCRApp()
    ocr_app.run()
