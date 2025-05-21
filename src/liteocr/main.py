import liteocr.resources_rc  # noqa: F401
import logging
from liteocr.logger_config import setup_logging

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QTranslator, QLibraryInfo
from liteocr.gui.config_window import ConfigWindow
from liteocr.gui.screenshot import ScreenshotOverlay
from liteocr.ocr_processor import OCRProcessor
from liteocr.config_manager import ConfigManager
from liteocr.gui.tray_icon_manager import TrayIconManager
from liteocr.hotkey_manager import HotkeyListenerThread
import pyperclip
from PySide6.QtCore import QThread, Signal


class OCRWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

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
    app: QtWidgets.QApplication

    def __init__(self):
        super().__init__()

        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.config_manager = ConfigManager()

        # Initialize translators
        self.qt_translator = QTranslator()
        self.app_translator = QTranslator()
        self._setup_translators()  # Load initial translations

        self.app.setQuitOnLastWindowClosed(False)
        self.config_window = None  # To store the active config window instance

        self.ocr_processor = None
        self.tray_icon_manager = TrayIconManager(
            settings_callback=self.show_settings, exit_callback=self.app.quit
        )
        try:
            self.tray_icon_manager.show()
            self.tray_icon_manager.update_texts()
        except Exception as e:
            logging.error(f"Error showing tray icon: {e}")

        self._initialize_ocr_processor()

        self.screenshot_overlay = None
        self.hotkey_listener_thread = None

        self._setup_hotkey_listener_thread()
        self._connect_signals()

        # Show startup notification
        config = self.config_manager.load_config()
        hotkey = config.get("hotkey", "<ctrl>+<alt>+s")
        self.tray_icon_manager.show_message(
            "LiteOCR",
            self.tr("LiteOCR has started in background.\nHotkey: ") + hotkey,
            "icon",
        )

    def _setup_hotkey_listener_thread(self):
        """Sets up and starts the hotkey listener thread."""
        self._teardown_hotkey_listener_thread()
        try:
            config = self.config_manager.load_config()
            hotkey_str = config.get("hotkey", "<ctrl>+<alt>+s")
            self.hotkey_listener_thread = HotkeyListenerThread(hotkey_str)
            self.hotkey_listener_thread.hotkey_activated.connect(
                self.capture_and_process
            )
            self.hotkey_listener_thread.start()
        except Exception as e:
            logging.error(f"Failed to set up hotkey listener thread: {e}")
            if self.tray_icon_manager:
                self.tray_icon_manager.show_message(
                    "LiteOCR Error",
                    self.tr("Failed to set up hotkey listener: ") + str(e),
                    "icon",
                )

    def _teardown_hotkey_listener_thread(self):
        """Stops the hotkey listener thread."""
        try:
            if self.hotkey_listener_thread and self.hotkey_listener_thread.isRunning():
                self.hotkey_listener_thread.stop_listener()
                self.hotkey_listener_thread = None
        except Exception as e:
            logging.error(f"Error tearing down hotkey listener thread: {e}")

    def _connect_signals(self):
        """Connects application signals to their respective slots."""
        self.app.aboutToQuit.connect(self._teardown_hotkey_listener_thread)

    def _initialize_ocr_processor(self):
        """Initializes or reinitializes the OCR processor based on the current configuration."""
        try:
            config = self.config_manager.load_config()
            api_key = config.get("api_key")
            provider = config.get("provider")

            if api_key and provider:
                self.ocr_processor = OCRProcessor(
                    str(provider),
                    str(api_key),
                    str(config.get("model", "")),
                    str(config.get("base_url", "")),
                )
            else:
                self.ocr_processor = None
        except Exception as e:
            logging.error(f"Error initializing OCR processor: {e}")
            self.ocr_processor = None
            if self.tray_icon_manager:
                self.tray_icon_manager.show_message(
                    "LiteOCR Error",
                    self.tr("Error initializing OCR processor: ") + str(e),
                    "icon",
                )

    def _setup_translators(self):
        """Sets up initial translations based on configuration or system locale."""
        config = self.config_manager.load_config()
        lang = config.get("language", "")
        if not lang:
            locale = QtCore.QLocale()
            lang = locale.name()
        self._load_translations(lang)

    def _load_translations(self, lang):
        """Loads Qt and application translations for the given language."""
        if not hasattr(self, "app"):
            logging.error("QApplication instance not found for translations.")
            return

        try:
            # Remove existing translators before loading new ones
            self.app.removeTranslator(self.qt_translator)
            self.app.removeTranslator(self.app_translator)

            # Load Qt base translations
            if self.qt_translator.load(
                "qt_" + lang,
                QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath),
            ):
                self.app.installTranslator(self.qt_translator)

            # Load application translations if not English
            if lang != "en_US":
                if self.app_translator.load(f":/translations/liteocr_{lang}.qm"):
                    self.app.installTranslator(self.app_translator)
                else:
                    logging.warning(
                        f"Could not load application translation file for language {lang}"
                    )
        except Exception as e:
            logging.error(f"Error loading translations for {lang}: {e}")

    def _show_screenshot_overlay(self):
        """Creates and shows the screenshot overlay."""
        try:
            self.screenshot_overlay = ScreenshotOverlay()
            self.screenshot_overlay.selection_captured.connect(
                self._process_captured_screenshot
            )
            self.screenshot_overlay.overlay_closed.connect(
                self._handle_screenshot_overlay_closed
            )
            self.screenshot_overlay.show()
            self.screenshot_overlay.activateWindow()
            self.screenshot_overlay.raise_()
        except Exception as e:
            logging.error(f"Error showing screenshot overlay: {e}")
            if self.tray_icon_manager:
                self.tray_icon_manager.show_message(
                    "LiteOCR Error",
                    self.tr("Error showing screenshot overlay: ") + str(e),
                    "icon",
                )

    def capture_and_process(self):
        """Initiates the screen capture process if OCR processor is ready."""
        if self.config_window and self.config_window.isVisible():
            logging.debug("Settings window is open. Hiding it for screenshot.")
            self.config_window.hide()

        if not self.ocr_processor:
            self.tray_icon_manager.show_message(
                "LiteOCR Error",
                self.tr("Please configure API key first."),
                "icon",
            )
            return
        self._show_screenshot_overlay()

    def _process_captured_screenshot(self, screenshot_pixmap):
        """Handles the captured screenshot pixmap asynchronously."""
        if not screenshot_pixmap:
            return

        # Create and start worker thread
        self.worker = OCRWorker(self.ocr_processor, screenshot_pixmap)
        self.worker.finished.connect(self._on_ocr_finished)
        self.worker.error.connect(self._on_ocr_error)
        self.worker.start()

    def _on_ocr_finished(self, latex_text):
        """Handles successful OCR completion."""
        try:
            pyperclip.copy(latex_text)
            self.tray_icon_manager.show_message(
                "LiteOCR", self.tr("LaTeX copied to clipboard!"), "icon"
            )
        except Exception as e:  # pyperclip can raise various errors
            logging.error(f"Error copying to clipboard: {e}")
            self.tray_icon_manager.show_message(
                "LiteOCR Error",
                self.tr("Failed to copy to clipboard: ") + str(e),
                "icon",
            )

    def _on_ocr_error(self, error_msg):
        """Handles OCR processing errors."""
        self.tray_icon_manager.show_message(
            "LiteOCR Error",
            self.tr("Failed to process image: ") + error_msg,
            "icon",
        )

    def _handle_screenshot_overlay_closed(self):
        """Restores the settings window if it was hidden for a screenshot."""
        if self.config_window and not self.config_window.isVisible():
            logging.debug("Screenshot overlay closed. Restoring settings window.")
            self.config_window.show()
            self.config_window.activateWindow()
            self.config_window.raise_()
        self.screenshot_overlay = None

    def _on_config_window_closed(self):
        """Called when the config window is closed."""
        logging.debug("Config window closed.")
        self.config_window = None

    def show_settings(self):
        if self.config_window:  # If already open, bring to front
            self.config_window.activateWindow()
            self.config_window.raise_()
            return

        try:
            self.config_window = ConfigWindow(config_manager=self.config_manager)
            self.config_window.finished.connect(self._on_config_window_closed)
            self.config_window.hotkey_changed.connect(self._on_hotkey_changed)
            result = self.config_window.exec()

            # If settings were saved, reinitialize OCRProcessor with new config and reload translations
            if result == QtWidgets.QDialog.DialogCode.Accepted:
                self._initialize_ocr_processor()

                current_config = self.config_manager.load_config()

                # Reload translations
                lang = current_config.get("language", "")
                if not lang:
                    locale = QtCore.QLocale()
                    lang = locale.name()
                self._load_translations(lang)

                # Update tray icon tooltip and menu items
                if self.tray_icon_manager:
                    self.tray_icon_manager.update_texts()

        except Exception as e:
            logging.error(f"Error in show_settings: {e}")
            if self.tray_icon_manager:
                self.tray_icon_manager.show_message(
                    "LiteOCR Error",
                    self.tr("Error opening settings or applying changes: ") + str(e),
                    "icon",
                )

    def _on_hotkey_changed(self, new_hotkey_str):
        """Handles the hotkey_changed signal from ConfigWindow."""
        self._teardown_hotkey_listener_thread()
        self._setup_hotkey_listener_thread()

    def run(self):
        try:
            self.app.exec()
        except Exception as e:
            logging.critical(f"Unhandled exception in LiteOCRApp.run: {e}")


def main():
    setup_logging()
    try:
        ocr_app = LiteOCRApp()
        ocr_app.run()
    except Exception as e:
        logging.critical(f"Critical error starting LiteOCR: {e}")


if __name__ == "__main__":
    main()
